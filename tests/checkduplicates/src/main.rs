//! A test for finding and managing duplicate facts across files.
use std::hash::{DefaultHasher, Hash, Hasher};

use clap::{command, Arg, ArgAction};
use indicatif::{ParallelProgressIterator, ProgressBar, ProgressStyle};
use rayon::iter::ParallelIterator;
use rayon::prelude::*;
use structures::{DuplicateFactMatch, FactClass, SIMILARITY_THRESHOLD};

use crate::structures::Fact;

mod structures;
mod util;

struct SerializedFact {
    original: Fact,
    token_hashes: Vec<u64>,
}

/// Hash something into a u64
#[inline(always)]
fn hash<T: Hash>(t: &T) -> u64 {
    let mut s = DefaultHasher::new();
    t.hash(&mut s);
    s.finish()
}

/// This function takes in two slices of sorted token hashes and computes the Dice-Sorensen
/// coefficient.
///
/// https://en.wikipedia.org/wiki/Dice-S%C3%B8rensen_coefficient#Formula
#[inline(always)]
fn dice_sorensen_sorted(set1: &[u64], set2: &[u64]) -> f64 {
    let len1 = set1.len();
    let len2 = set2.len();

    let mut intersect = 0;
    let mut i = 0;
    let mut j = 0;

    // calculate the intersection of the two sorted vecs of tokens:
    // https://stackoverflow.com/questions/42538902/how-to-intersect-two-sorted-arrays-the-fastest-possible-way
    while i < len1 && j < len2 {
        let x = set1[i];
        let y = set2[j];

        if x == y {
            intersect += 1;
            i += 1;
            j += 1;
        } else if x < y {
            i += 1;
        } else {
            j += 1;
        }
    }

    // DSC = (2|X intersect Y|)/(|X| + |Y|)
    (2.0 * intersect as f64) / ((len1 + len2) as f64) * 100.0
}

/// Finds duplicate facts across safe and unsafe fact files using parallel processing.
///
/// This function:
/// 1. Loads facts from both safe.txt and unsafe.txt
/// 2. Generates all possible pairs of facts
/// 3. Calculates similarity ratios in parallel
/// 4. Returns matches above the similarity threshold
///
/// # Returns
/// A vector of DuplicateFactMatch containing similar fact pairs and their similarity scores
fn find_duplicate_facts() -> Vec<DuplicateFactMatch> {
    // read safe.txt and unsafe.txt into lists
    let mut all_facts = util::load_fact_list("safe.txt", FactClass::Safe);
    let mut unsafe_contents = util::load_fact_list("unsafe.txt", FactClass::Unsafe);

    all_facts.append(&mut unsafe_contents);

    // serialize each fact by:
    // tokenizing, filtering junk, hashing, and sorting
    let mut facts: Vec<SerializedFact> = all_facts
        .into_iter()
        .map(|f| {
            let mut hashes: Vec<u64> = f
                .fact
                .split_whitespace()
                .filter_map(|tok| {
                    let normalized = tok
                        .chars()
                        .filter(char::is_ascii_alphanumeric)
                        .collect::<String>()
                        .to_ascii_lowercase();

                    if normalized.is_empty() {
                        None
                    } else {
                        Some(hash(&normalized))
                    }
                })
                .collect();

            // sort hashes so we can do a linear list intersect
            hashes.sort_unstable();
            // remove duplicates (dice sorensen expects a set)
            hashes.dedup();

            SerializedFact {
                original: f,
                token_hashes: hashes,
            }
        })
        .collect();

    // this will compare things that are of similar lengths first so that we can break out of the
    // sliding window early once its mathematically impossible to be the same
    facts.sort_unstable_by_key(|f| f.token_hashes.len());

    // Initialize progress bar with custom style
    let pb = ProgressBar::new(facts.len() as u64);
    pb.set_style(
        ProgressStyle::default_bar()
            .template(
                "{percent}% |{wide_bar}| {pos}/{len} [{elapsed_precise}<{eta_precise} {per_sec}]",
            )
            .unwrap(),
    );

    // when two things are different enough in length, they cannot be the same mathematically based
    // on the similarity threshold.
    //
    // - DSC = (2 * X intersect Y)/(|X| + |Y|)
    // - since the list is sorted, we know that len1 <= len2, so the maximum possible intersection
    //   between the two sets is len1
    // - (2*len1)/(len1 + len2) >= threshold
    //   (2*len1) >= threshold*(len1 + len2)
    //   2*len1 >= threshold*len1 + threshold*len2
    //   2*len1 - threshold*len1 >= threshold*len2
    //   len1*(2 - threshold) >= threshold*len2
    //   len1*(2 - threshold)/threshold >= len2
    let fractional_ratio = SIMILARITY_THRESHOLD / 100.0;
    let length_diff_ratio = (2.0 - fractional_ratio) / fractional_ratio;

    // Process facts in parallel
    facts
        .par_iter()
        .enumerate()
        .progress_with(pb)
        .flat_map(|(i, f1)| {
            let mut matches = vec![];
            let len1 = f1.token_hashes.len();

            for f2 in &facts[i + 1..] {
                let len2 = f2.token_hashes.len();

                // if lengths are too different to possibly be the same, don't try any of the
                // remaining facts
                if (len2 as f64) > (len1 as f64) * length_diff_ratio {
                    break;
                }

                let ratio = dice_sorensen_sorted(&f1.token_hashes, &f2.token_hashes);
                if ratio > SIMILARITY_THRESHOLD {
                    matches.push((f1.original.clone(), f2.original.clone(), ratio));
                }
            }

            matches
        })
        .collect()
}

fn main() {
    let args = command!()
        .arg(
            Arg::new("fix_duplicates")
                .long("fix-duplicates")
                .action(ArgAction::SetTrue)
                .help("Remove duplicate facts"),
        )
        .get_matches();

    let matches = find_duplicate_facts();

    if !matches.is_empty() {
        if !args.get_flag("fix_duplicates") {
            println!("{:#?}", matches);
            println!("\nNumber of similar facts: {}", matches.len());
            std::process::exit(1);
        }

        // Fix mode: Remove duplicates
        println!("Generating list of indicies to remove...");
        let mut indicies_to_remove = vec![];

        // Determine which facts to remove, prioritizing keeping unsafe facts
        for fact_match in matches {
            println!("{:#?}", fact_match);

            // keep unsafe facts over safe facts
            if fact_match.0.class == FactClass::Unsafe {
                indicies_to_remove.push((fact_match.0.line_number, fact_match.0.class));
            } else {
                // first fact isn't unsafe so we don't need to prioritize it
                indicies_to_remove.push((fact_match.1.line_number, fact_match.1.class));
            }
        }

        // Load current facts
        let mut safe_facts = util::load_fact_list("safe.txt", FactClass::Safe);
        let mut unsafe_facts = util::load_fact_list("unsafe.txt", FactClass::Unsafe);

        // sort removal indicies in reverse to maintain correct line numbers
        indicies_to_remove.sort_unstable_by(|a, b| b.0.cmp(&a.0));
        indicies_to_remove.dedup();

        // Remove duplicates from respective files
        for (index, class) in indicies_to_remove {
            match class {
                FactClass::Safe => safe_facts.remove(index),
                FactClass::Unsafe => unsafe_facts.remove(index),
            };
        }

        // Write updated facts back to files
        util::write_facts_to_file("safe.txt", &safe_facts);
        util::write_facts_to_file("unsafe.txt", &unsafe_facts);
    }
}
