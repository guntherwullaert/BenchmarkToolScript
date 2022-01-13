from pathlib import Path
import shutil, sys, subprocess

# Generates the run script for the benchmark tool and returns it
def generate_run_script():
    output_folder = "output"
    machine_name = "default-machine"
    machine_cpu = "24x8xE5520@2.27GHz"
    machine_memory = "24GB"
    config_name = "seq-generic"
    config_template = "seq-generic.sh"
    solver = "clingo"
    solver_version = "4.5.4"
    solver_measures = "clasp"
    solver_flags = "--stats --quiet=1,0"
    job_name = "seq-gen"
    job_timeout = "900"
    job_runs = "1"
    job_script_mode = "timeout"
    job_walltime="50:00:00"
    job_parallel = "1"
    benchmark_name = "test"
    benchmark_path = "../benchmarks"
    project_name = "clingo-seq-job"
    
    return f"<runscript output='{output_folder}'>\n \
    <machine name='{machine_name}' cpu='{machine_cpu}' memory='{machine_memory}' />\n \
    <config name='{config_name}' template='{config_template}' />\n\
    <system name='{solver}' version='{solver_version}' measures='{solver_measures}' config='{config_name}'>\n\
        <setting name='setting-1' cmdline='{solver_flags}' tag='basic' />\n\
    </system>\n\
    <seqjob name='{job_name}' timeout='{job_timeout}' runs='{job_runs}' script_mode='{job_script_mode}' walltime='{job_walltime}' parallel='{job_parallel}' />\n\
    <benchmark name='{benchmark_name}'>\n\
        <folder path='{benchmark_path}'></folder>\n\
    </benchmark>\n\
    <project name='{project_name}' job='{job_name}'>\n\
        <runtag machine='{machine_name}' benchmark='{benchmark_name}' tag='basic' />\n\
    </project>\n\
</runscript>"

# generates the run script and puts it in a file and in the correct location
def create_run_script():
    with open("btool/runscript.xml", "w") as text_file:
        text_file.write(generate_run_script())

def generate_program():
    return f"#!/bin/bash\n\
    \n\
    exec clingo \"${{@}}\" 2> solver.err"

def create_program():
    program_name = "clingo"
    program_version= "4.5.4"
    with open(f"btool/programs/{program_name}-{program_version}", "w") as text_file:
        text_file.write(generate_program())

def create_folder_structure():
    Path("btool/programs").mkdir(parents=True, exist_ok=True)

def copy_benchmark_tool_files():
    shutil.copyfile("setup_files/seq-generic.sh", "btool/seq-generic.sh")
    shutil.copyfile("setup_files/bconv", "btool/bconv")
    shutil.copyfile("setup_files/beval", "btool/beval")
    shutil.copyfile("setup_files/bfeat", "btool/bfeat")
    shutil.copyfile("setup_files/bgen", "btool/bgen")
    shutil.copyfile("setup_files/bstats", "btool/bstats")
    shutil.copyfile("setup_files/mount-zip", "btool/mount-zip")
    shutil.copyfile("setup_files/gcat.sh", "btool/programs/gcat.sh")
    shutil.copyfile("setup_files/runsolver-3.3.4", "btool/programs/runsolver-3.3.4")
    shutil.copytree("setup_files/src", "btool/src", dirs_exist_ok=True)

def setup():
    create_folder_structure()
    create_run_script()
    copy_benchmark_tool_files()
    create_program()
    out = subprocess.run(['./bgen', 'runscript.xml'], cwd='btool')
    print(out)

def run():
    subprocess.run(['python3', 'output/clingo-seq-job/default-machine/start.py'], cwd='btool')
    subprocess.run(['./beval', 'runscript.xml'], cwd='btool')

if len(sys.argv) < 2:
    print("Usage: setup_benchmark_project [command]")
    exit()

if(sys.argv[1] == "setup"):
    setup()

if(sys.argv[1] == "run"):
    run()