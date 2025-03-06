import os
import subprocess
import csv
import sys

atom_list = os.path.join(os.path.dirname(__file__), "atom_list")
functionals = ["O3LYP", "pbe0", "camB3LYP", "M062X"]
template = os.path.join(os.path.dirname(__file__), "dens_ana_template")

hostname = os.uname().nodename

if "atlas" in hostname:
    Host = "hpc"
    scratch = "/hpctmp/e0732532"
    ORCA_ROOT = "/app1/ebapps/arches/flat/software/ORCA/6.0.1-foss-2023b/bin/"
    THEO_ROOT = "/home/svu/e0732532/software/TheoDORE_3.2"
    template = "/home/svu/e0732532/bin/dens_ana_template"
elif "asp2a" in hostname:
    Host = "nscc"
    scratch = f"/home/users/nus/{os.getenv('USER')}/orca_6_0_0"
    ORCA_ROOT = "/home/project/11004127/software/orca601_avx2"
    THEO_ROOT = "/home/users/nus/e0732533/Software/TheoDORE_3.2"
    template = "/home/users/nus/e0732533/bin/dens_ana_template"
elif "Precision" in hostname:
    Host = "bohr"
    scratch = "/home/scratch/hanqi/orca"

template = os.path.join(os.path.dirname(__file__), "dens_ana_template")

molecule_list = []
accepter_list = []
donor1_list = []
donor2_list = []

with open(atom_list, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        molecule_list.append(row[0])
        accepter_list.append(row[1])
        donor1_list.append(row[2])
        donor2_list.append(row[3])

if len(sys.argv) > 1:
    molecule_list = [sys.argv[1]]
    index = molecule_list.index(sys.argv[1])
    accepter_list = [accepter_list[index]]
    donor1_list = [donor1_list[index]]
    donor2_list = [donor2_list[index]]

with open('theo_ana.csv', 'w', newline='') as csvfile:
    fieldnames = ["Molecule_Name", "Functional", "HOMO", "Theodore_EHD1", "Theodore_EHD2", "Theodore_EHD3", "Gap1", "Gap2", "Gap3", "CT1", "CT2", "CT3", "S1_Initial_1", "S1_Initial_2", "S1_Initial_3", "S1_Final_1", "S1_Final_2", "S1_Final_3", "T1_Initial_1", "T1_Initial_2", "T1_Initial_3", "T1_Final_1", "T1_Final_2", "T1_Final_3", "S1_Dscf_Initial", "S1_Dscf_Final", "S2_Dscf_Initial", "S2_Dscf_Final", "PRNTO_ST", "CT_ST"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i, molecule in enumerate(molecule_list):
        accepter = accepter_list[i]
        donor1 = donor1_list[i]
        donor2 = donor2_list[i]

        if len(sys.argv) == 1:
            os.chdir(molecule)

        for func in functionals:
            FLUO = f"{molecule}_{func}_svp_s1_tddft_scf"
            DSCF_S1 = f"{molecule}_{func}_svp_s1_Dscf_optfreq"
            DSCF_S2 = f"{molecule}_{func}_svp_s2_Dscf_optfreq"

            subprocess.run([f"{ORCA_ROOT}/orca_2mkl", FLUO, "-molden"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            with open(f"den_ana_{FLUO}.in", 'w') as f:
                with open(template, 'r') as template_file:
                    for line in template_file:
                        line = line.replace("NAME", FLUO).replace("DONOR", donor1).replace("ACCEPTOR", accepter)
                        f.write(line)

            HOMO = subprocess.check_output(["ORCA-GrepHOMO", "-q", f"{FLUO}.out"]).decode().strip()

            S1_Initial_1 = subprocess.check_output(["ORCA-GrepExcitation", "-i", f"{FLUO}.out"]).decode().strip()
            S1_Initial_2 = subprocess.check_output(["ORCA-GrepExcitation", "-i", "-s", "2", f"{FLUO}.out"]).decode().strip()
            S1_Initial_3 = subprocess.check_output(["ORCA-GrepExcitation", "-i", "-s", "3", f"{FLUO}.out"]).decode().strip()
            S1_Final_1 = subprocess.check_output(["ORCA-GrepExcitation", "-f", f"{FLUO}.out"]).decode().strip()
            S1_Final_2 = subprocess.check_output(["ORCA-GrepExcitation", "-f", "-s", "2", f"{FLUO}.out"]).decode().strip()
            S1_Final_3 = subprocess.check_output(["ORCA-GrepExcitation", "-f", "-s", "3", f"{FLUO}.out"]).decode().strip()
            T1_Initial_1 = subprocess.check_output(["ORCA-GrepExcitation", "-i", "-s", "11", f"{FLUO}.out"]).decode().strip()
            T1_Initial_2 = subprocess.check_output(["ORCA-GrepExcitation", "-i", "-s", "12", f"{FLUO}.out"]).decode().strip()
            T1_Initial_3 = subprocess.check_output(["ORCA-GrepExcitation", "-i", "-s", "13", f"{FLUO}.out"]).decode().strip()
            T1_Final_1 = subprocess.check_output(["ORCA-GrepExcitation", "-f", "-s", "11", f"{FLUO}.out"]).decode().strip()
            T1_Final_2 = subprocess.check_output(["ORCA-GrepExcitation", "-f", "-s", "12", f"{FLUO}.out"]).decode().strip()
            T1_Final_3 = subprocess.check_output(["ORCA-GrepExcitation", "-f", "-s", "13", f"{FLUO}.out"]).decode().strip()

            if os.path.isfile(f"{DSCF_S1}.out"):
                S1_Dscf_Initial = subprocess.check_output(["ORCA-chkOrbital", "-q", f"{DSCF_S1}.out"]).decode().split()[0]
                S1_Dscf_Final = subprocess.check_output(["ORCA-chkOrbital", "-q", f"{DSCF_S1}.out"]).decode().split()[2]
            else:
                S1_Dscf_Initial = 0
                S1_Dscf_Final = 0

            if os.path.isfile(f"{DSCF_S2}.out"):
                S2_Dscf_Initial = subprocess.check_output(["ORCA-chkOrbital", "-q", f"{DSCF_S2}.out"]).decode().split()[0]
                S2_Dscf_Final = subprocess.check_output(["ORCA-chkOrbital", "-q", f"{DSCF_S2}.out"]).decode().split()[2]
            else:
                S2_Dscf_Initial = 0
                S2_Dscf_Final = 0

            subprocess.run([f"{ORCA_ROOT}/orca_2mkl", FLUO, "-molden"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["cp", f"{FLUO}.cis", "orca.cis"])

            subprocess.run(["theodore", "analyze_tden", "-f", f"den_ana_{FLUO}.in"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            EHD1 = subprocess.check_output(["grep", "1(1)A", f"theo_{FLUO}.txt"]).decode().split()[8]
            EHD2 = subprocess.check_output(["grep", "2(1)A", f"theo_{FLUO}.txt"]).decode().split()[8]
            EHD3 = subprocess.check_output(["grep", "3(1)A", f"theo_{FLUO}.txt"]).decode().split()[8]
            gap1 = subprocess.check_output(["grep", "1(1)A", f"theo_{FLUO}.txt"]).decode().split()[1]
            gap2 = subprocess.check_output(["grep", "2(1)A", f"theo_{FLUO}.txt"]).decode().split()[1]
            gap3 = subprocess.check_output(["grep", "3(1)A", f"theo_{FLUO}.txt"]).decode().split()[1]
            CT1 = subprocess.check_output(["grep", "1(1)A", f"theo_{FLUO}.txt"]).decode().split()[6]
            CT2 = subprocess.check_output(["grep", "2(1)A", f"theo_{FLUO}.txt"]).decode().split()[6]
            CT3 = subprocess.check_output(["grep", "3(1)A", f"theo_{FLUO}.txt"]).decode().split()[6]

            subprocess.run(["theodore", "analyze_tden_es2es", "-r", "1", "-f", f"den_ana_{FLUO}.in"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            CT_ST = subprocess.check_output(["grep", "1(3)A", f"summ_den_ana_es2es_{FLUO}.txt"]).decode().split()[6]
            PRNTO_ST = subprocess.check_output(["grep", "1(3)A", f"summ_den_ana_es2es_{FLUO}.txt"]).decode().split()[13]

            writer.writerow({
                "Molecule_Name": molecule,
                "Functional": func,
                "HOMO": HOMO,
                "Theodore_EHD1": EHD1,
                "Theodore_EHD2": EHD2,
                "Theodore_EHD3": EHD3,
                "Gap1": gap1,
                "Gap2": gap2,
                "Gap3": gap3,
                "CT1": CT1,
                "CT2": CT2,
                "CT3": CT3,
                "S1_Initial_1": S1_Initial_1,
                "S1_Initial_2": S1_Initial_2,
                "S1_Initial_3": S1_Initial_3,
                "S1_Final_1": S1_Final_1,
                "S1_Final_2": S1_Final_2,
                "S1_Final_3": S1_Final_3,
                "T1_Initial_1": T1_Initial_1,
                "T1_Initial_2": T1_Initial_2,
                "T1_Initial_3": T1_Initial_3,
                "T1_Final_1": T1_Final_1,
                "T1_Final_2": T1_Final_2,
                "T1_Final_3": T1_Final_3,
                "S1_Dscf_Initial": S1_Dscf_Initial,
                "S1_Dscf_Final": S1_Dscf_Final,
                "S2_Dscf_Initial": S2_Dscf_Initial,
                "S2_Dscf_Final": S2_Dscf_Final,
                "PRNTO_ST": PRNTO_ST,
                "CT_ST": CT_ST
            })

        if len(sys.argv) == 1:
            os.chdir("..")