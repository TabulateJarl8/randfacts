use std::{
    fs::File,
    io::{BufRead, BufReader, BufWriter, Write},
    path::PathBuf,
    process::Command,
};

use crate::structures::{Fact, FactClass};

/// Get a file from the randfacts/ directory in the top level of the project
///
/// # Arguments
///
/// * `filename` - the filename to find.
///
/// # Panics
///
/// This function will panic if a file that doesn't exist is requested
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

/// Given an array of facts, write them separated with newlines to a file.
///
/// # Arguments
///
/// * `filename` - the filename in `randfacts/` to write to
/// * `facts` - The array of facts to write
pub fn write_facts_to_file(filename: &str, facts: &[Fact]) {
    let file = File::create(get_project_path(filename)).expect("no such file");
    let mut writer = BufWriter::new(file);

    for fact in facts {
        writeln!(writer, "{}", fact.fact).expect("error writing file");
    }
}

/// Read facts from a file into a vector.
///
/// # Arguments
///
/// * `filename` - the file in `randfacts/` to read from
/// * `fact_class` - The class of the facts (safe or unsafe)
pub fn load_fact_list(filename: &str, fact_class: FactClass) -> Vec<Fact> {
    let file = File::open(get_project_path(filename)).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .enumerate()
        .map(|(line_number, line)| {
            Fact::new(line.expect("Could not parse line"), fact_class, line_number)
        })
        .collect()
}
