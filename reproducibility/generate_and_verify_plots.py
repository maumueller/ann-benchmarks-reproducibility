import glob
import os


fns = glob.glob(os.path.join("paper", "*.tex.template"))

missing = []

for fn in fns:
    with open(fn) as f:
        with open(fn[:-9], "w") as g:
            for line in f:
                if "%%PROCESS" not in line:
                    g.write(line)
                else:
                    line = line.strip()[10:] 
                    label, attributes = None, None
                    if "[" in line:
                        other, attributes = line.split("[")
                        attributes = attributes[:-1]
                        gn, label = other.split()
                    else:
                        if " " in line:
                            gn, *label = line.split()
                            label = " ".join(label)
                        else:
                            gn = line
                    if os.path.exists(os.path.join("paper", gn)):
                        s = "\\addplot"
                        if attributes:
                            s += "[" + attributes + "]"
                        s += " table {" + gn + "};"
                        g.write(s + "\n")
                        if label:
                            g.write("\\addlegendentry{%s};\n" % label)
                    else:
                        missing.append(gn)

print("Done processing all files. %d files were missing" % len(missing))

if len(missing) > 0:
    print("The following files were missing:")
    print("\n".join(missing))
                
#\addplot table {result_tables/sift-128-euclidean_10_faiss-ivf-gpu-batch_k-nn_qps};
#\addlegendentry{ FAI-IVF-GPU };