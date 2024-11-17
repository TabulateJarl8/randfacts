use std::{
    fmt,
    fs::File,
    io::{BufRead, BufReader, Write},
    path::PathBuf,
    process::Command,
    sync::Arc,
};

use clap::{command, Arg, ArgAction};
use indicatif::{ParallelProgressIterator, ProgressBar, ProgressStyle};
use itertools::Itertools;
use rayon::iter::ParallelIterator;
use rayon::prelude::*;

type DuplicateFactMatch = (Fact, Fact, f64);
const INITIAL_VEC_CAPACITY: usize = 1000;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum FactClass {
    Safe,
    Unsafe,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct Fact {
    fact: Arc<String>,
    class: FactClass,
    line_number: usize,
}

impl Fact {
    pub fn new(fact: String, class: FactClass, line_number: usize) -> Self {
        Self {
            fact: Arc::new(fact),
            class,
            line_number,
        }
    }
}

impl fmt::Display for FactClass {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            FactClass::Safe => write!(f, "Safe"),
            FactClass::Unsafe => write!(f, "Unsafe"),
        }
    }
}

#[inline(always)]
fn token_sort_ratio(str1: &str, str2: &str) -> f64 {
    // Preallocate vectors with capacity
    let mut vec1 = Vec::with_capacity(INITIAL_VEC_CAPACITY);
    let mut vec2 = Vec::with_capacity(INITIAL_VEC_CAPACITY);

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

    let mut prev_row = (0..=len2).collect::<Vec<_>>();
    let mut curr_row = vec![0; len2 + 1];

    // Initialize first row
    for i in 0..=len2 {
        prev_row[i] = i;
    }

    for (i, c1) in s1.iter().enumerate() {
        curr_row[0] = i + 1;

        for (j, c2) in s2.iter().enumerate() {
            curr_row[j + 1] = if c1 == c2 {
                prev_row[j]
            } else {
                1 + prev_row[j].min(prev_row[j + 1]).min(curr_row[j])
            };
        }

        // Swap rows using copy_from_slice for better performance
        prev_row[..=len2].copy_from_slice(&curr_row[..=len2]);
    }

    prev_row[len2]
}

fn get_project_path(filename: &str) -> PathBuf {
    // get project's top level
    let output = Command::new("git")
        .args(["rev-parse", "--show-toplevel"])
        .output()
        .expect("failed to execute git process");

    if !output.status.success() {
        panic!("Error:  {}", String::from_utf8_lossy(&output.stderr));
    }

    let mut project_root: PathBuf = PathBuf::from(String::from_utf8(output.stdout).unwrap().trim());

    project_root.push("randfacts");
    project_root.push(filename);
    project_root
}

fn write_facts_to_file(filename: &str, facts: Vec<Fact>) {
    let mut file = File::create(get_project_path(filename)).expect("no such file");
    for fact in facts {
        writeln!(file, "{}", fact.fact).expect("error writing file");
    }
}

fn load_fact_list(filename: &str, comment: FactClass) -> Vec<Fact> {
    let file = File::open(get_project_path(filename)).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .enumerate()
        .map(|(line_number, line)| {
            Fact::new(line.expect("Could not parse line"), comment, line_number)
        })
        .collect()
}

fn find_duplicate_facts() -> Vec<DuplicateFactMatch> {
    // read safe.txt and unsafe.txt into lists
    let mut all_facts = load_fact_list("safe.txt", FactClass::Safe);

    let mut unsafe_contents = load_fact_list("unsafe.txt", FactClass::Unsafe);

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

    // iterate through all the combinations
    let matches: Vec<_> = all_facts
        .into_iter()
        .combinations(2)
        .par_bridge()
        .progress_with(pb)
        .filter_map(|facts| {
            let ratio = token_sort_ratio(&facts[0].fact, &facts[1].fact);
            if ratio > 82.5 {
                Some((facts[0].clone(), facts[1].clone(), ratio))
            } else {
                None
            }
        })
        .collect();
    matches
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
            let mut safe_facts = load_fact_list("safe.txt", FactClass::Safe);
            let mut unsafe_facts = load_fact_list("unsafe.txt", FactClass::Unsafe);

            // sort removal indicies in reverse so that file lines dont get messed up
            indicies_to_remove.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());

            // remove one of the duplicate facts from the files
            for (index, class) in indicies_to_remove {
                _ = match class {
                    FactClass::Safe => safe_facts.remove(index),
                    FactClass::Unsafe => unsafe_facts.remove(index),
                }
            }

            write_facts_to_file("safe.txt", safe_facts);
            write_facts_to_file("unsafe.txt", unsafe_facts);
        }
    }
}
