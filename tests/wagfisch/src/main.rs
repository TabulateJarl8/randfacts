use std::{
    fs::File,
    io::{BufRead, BufReader},
    path::PathBuf,
    process::Command,
};

use clap::{command, Arg, ArgAction};
use indicatif::{ParallelProgressIterator, ProgressBar, ProgressStyle};
use itertools::Itertools;
use rayon::iter::ParallelIterator;
use rayon::prelude::*;

#[inline(always)]
fn token_sort_ratio(str1: &str, str2: &str) -> f64 {
    // Preallocate vectors with capacity
    let mut vec1 = Vec::with_capacity(str1.len());
    let mut vec2 = Vec::with_capacity(str2.len());

    // Filter and collect characters in one pass
    str1.chars()
        .filter(|c| c.is_ascii_alphanumeric())
        .for_each(|c| vec1.push(c));
    str2.chars()
        .filter(|c| c.is_ascii_alphanumeric())
        .for_each(|c| vec2.push(c));

    // Calculate Levenshtein distance directly on character vectors
    let dist = wagner_fischer_2row(&vec1, &vec2) as f64;
    let maximum = vec1.len() + vec2.len();

    if maximum == 0 {
        return 0.0;
    }

    (1.0 - (dist / maximum as f64)) * 100.0 - 5.0
}

// Custom Levenshtein implementation optimized for our use case
#[inline(always)]
fn levenshtein(s1: &[char], s2: &[char]) -> usize {
    if s1.len() > s2.len() {
        return levenshtein(s2, s1);
    }

    let len1 = s1.len();
    let len2 = s2.len();

    let mut column = Vec::with_capacity(len1 + 1);
    for i in 0..=len1 {
        column.push(i);
    }

    for j in 1..=len2 {
        let mut previous = column[0];
        column[0] = j;

        for i in 1..=len1 {
            let old = column[i];
            column[i] = if s1[i - 1] == s2[j - 1] {
                previous
            } else {
                1 + previous.min(column[i - 1]).min(column[i])
            };
            previous = old;
        }
    }

    column[len1]
}

#[inline(always)]
fn wagner_fischer_2row(s1: &[char], s2: &[char]) -> usize {
    let len1 = s1.len();
    let len2 = s2.len();

    if len1 == 0 {
        return len2;
    }
    if len2 == 0 {
        return len1;
    }

    let mut prev_row = (0..=len2).collect::<Vec<_>>();
    let mut curr_row = vec![0; len2 + 1];

    for i in 1..=len1 {
        curr_row[0] = i;
        for j in 1..=len2 {
            curr_row[j] = if s1[i - 1] == s2[j - 1] {
                prev_row[j - 1]
            } else {
                1 + prev_row[j - 1].min(prev_row[j]).min(curr_row[j - 1])
            };
        }
        std::mem::swap(&mut prev_row, &mut curr_row);
    }

    prev_row[len2]
}

fn lines_from_file(filename: &PathBuf, comment: &str) -> Vec<(String, String)> {
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| (l.expect("Could not parse line"), comment.to_string()))
        .collect()
}

fn main() {
    let m = command!()
        .arg(
            Arg::new("fix_duplicates")
                .long("fix-duplicates")
                .action(ArgAction::SetTrue)
                .help("Remove duplicate facts"),
        )
        .get_matches();

    // get project's top level
    let output = Command::new("git")
        .args(["rev-parse", "--show-toplevel"])
        .output()
        .expect("failed to execute git process");

    if !output.status.success() {
        panic!("Error:  {}", String::from_utf8_lossy(&output.stderr));
    }

    // read safe.txt and unsafe.txt into lists
    let mut project_root: PathBuf = PathBuf::from(String::from_utf8(output.stdout).unwrap().trim());
    project_root.push("randfacts");
    project_root.push("safe.txt");

    let mut all_facts = lines_from_file(&project_root, "safe");

    project_root.pop();
    project_root.push("unsafe.txt");

    let mut unsafe_contents = lines_from_file(&project_root, "unsafe");

    all_facts.append(&mut unsafe_contents);

    // Generate all possible pairs of the facts from safe.txt and unsafe.txt
    // combined
    let total_facts = all_facts.len() as u64;
    let total_combinations = num_integer::binomial(total_facts, 2);
    println!("facts: {}, comb: {}", total_facts, total_combinations);

    let pb = ProgressBar::new(total_combinations);
    pb.set_style(
        ProgressStyle::default_bar()
            .template(
                "{percent}% |{wide_bar}| {pos}/{len} [{elapsed_precise}<{eta_precise} {per_sec}]",
            )
            .unwrap(),
    );

    // iterate through all the combinations
    let matches: Vec<_> = all_facts
        .into_iter()
        .combinations(2)
        .par_bridge()
        .progress_with(pb)
        .filter_map(|facts| {
            let ratio = token_sort_ratio(&facts[0].0, &facts[1].0);
            if ratio > 82.5 {
                Some((facts[0].clone(), facts[1].clone(), ratio))
            } else {
                None
            }
        })
        .collect();
}
