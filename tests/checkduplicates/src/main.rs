use clap::{command, Arg, ArgAction};
use indicatif::{ParallelProgressIterator, ProgressBar, ProgressStyle};
use rayon::iter::ParallelIterator;
use rayon::prelude::*;
use structures::{DuplicateFactMatch, FactClass, SIMILARITY_THRESHOLD};

mod structures;
mod util;

#[inline(always)]
fn token_sort_ratio(str1: &str, str2: &str) -> f64 {
    let len1 = str1.len();
    let len2 = str2.len();

    // Early exit for obviously different strings
    // if their lengths differ by more than half, they're most likely different enough
    // this may lead to issues, but it lead to a ~23.33% performance improvement
    if (len1 as f64 / len2 as f64) < 0.5 || (len2 as f64 / len1 as f64) < 0.5 {
        return 0.0;
    }

    // Preallocate vectors with capacity
    let mut vec1 = Vec::with_capacity(len1);
    let mut vec2 = Vec::with_capacity(len2);

    // Filter and collect characters in one pass
    str1.chars()
        .filter(|c| c.is_ascii_alphanumeric())
        .for_each(|c| vec1.push(c.to_ascii_lowercase()));
    str2.chars()
        .filter(|c| c.is_ascii_alphanumeric())
        .for_each(|c| vec2.push(c.to_ascii_lowercase()));

    // Calculate wagner fischer directly on character vectors
    let dist = wagner_fischer_2row(&vec1, &vec2) as f64;
    let maximum = vec1.len() + vec2.len();

    if maximum == 0 {
        return 0.0;
    }

    (1.0 - (dist / maximum as f64)) * 100.0 - 5.0
}

#[inline(always)]
fn wagner_fischer_2row(s1: &[char], s2: &[char]) -> usize {
    // Always make s1 the shorter string
    let (s1, s2) = if s1.len() < s2.len() {
        (s1, s2)
    } else {
        (s2, s1)
    };

    let len1 = s1.len();
    let len2 = s2.len();

    if len1 == 0 {
        return len2;
    }
    if len2 == 0 {
        return len1;
    }

    let mut prev_row = vec![0; len2 + 1];
    let mut curr_row = vec![0; len2 + 1];

    // Initialize first row
    (0..=len2).for_each(|i| {
        prev_row[i] = i;
    });

    for (i, c1) in s1.iter().enumerate() {
        curr_row[0] = i + 1;

        for (j, c2) in s2.iter().enumerate() {
            curr_row[j + 1] = if c1 == c2 {
                prev_row[j]
            } else {
                1 + prev_row[j].min(prev_row[j + 1]).min(curr_row[j])
            };
        }

        // Swap rows using mem::swap for better performance
        std::mem::swap(&mut prev_row, &mut curr_row);
    }

    prev_row[len2]
}

fn find_duplicate_facts() -> Vec<DuplicateFactMatch> {
    // read safe.txt and unsafe.txt into lists
    let mut all_facts = util::load_fact_list("safe.txt", FactClass::Safe);

    let mut unsafe_contents = util::load_fact_list("unsafe.txt", FactClass::Unsafe);

    all_facts.append(&mut unsafe_contents);

    // Generate all possible pairs of the facts from safe.txt and unsafe.txt
    // combined
    let total_facts = all_facts.len() as u64;
    let total_combinations = num_integer::binomial(total_facts as u64, 2);

    let pb = ProgressBar::new(total_combinations);
    pb.set_style(
        ProgressStyle::default_bar()
            .template(
                "{percent}% |{wide_bar}| {pos}/{len} [{elapsed_precise}<{eta_precise} {per_sec}]",
            )
            .unwrap(),
    );

    // Generate all possible indices combinations
    let indices: Vec<_> = (0..all_facts.len())
        .flat_map(|i| ((i + 1)..all_facts.len()).map(move |j| (i, j)))
        .collect();

    // Process combinations in parallel
    indices
        .into_par_iter()
        .progress_with(pb)
        .filter_map(|(i, j)| {
            let facts = &all_facts;
            let fact1 = &facts[i];
            let fact2 = &facts[j];

            let ratio = token_sort_ratio(&fact1.fact, &fact2.fact);
            if ratio > SIMILARITY_THRESHOLD {
                Some((fact1.clone(), fact2.clone(), ratio))
            } else {
                None
            }
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
        } else {
            println!("Generating list of indicies to remove...");
            let mut indicies_to_remove = vec![];
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

            // remove all indicies from combinations
            let mut safe_facts = util::load_fact_list("safe.txt", FactClass::Safe);
            let mut unsafe_facts = util::load_fact_list("unsafe.txt", FactClass::Unsafe);

            // sort removal indicies in reverse so that file lines dont get messed up
            indicies_to_remove.sort_unstable_by(|a, b| b.0.partial_cmp(&a.0).unwrap());

            // remove one of the duplicate facts from the files
            for (index, class) in indicies_to_remove {
                match class {
                    FactClass::Safe => safe_facts.remove(index),
                    FactClass::Unsafe => unsafe_facts.remove(index),
                };
            }

            util::write_facts_to_file("safe.txt", &safe_facts);
            util::write_facts_to_file("unsafe.txt", &unsafe_facts);
        }
    }
}
