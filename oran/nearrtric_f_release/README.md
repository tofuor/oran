git clone "https://gerrit.o-ran-sc.org/r/ric-plt/ric-dep"

cd ric-dep/bin
./install_k8s_and_helm.sh

./install_common_templates_to_helm.sh