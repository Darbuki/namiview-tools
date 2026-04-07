import utils
import kubernetes_utils
from concurrent.futures import ThreadPoolExecutor

VAULT_PODS_LABEL = "app.kubernetes.io/name=vault"
VAULT_PODS_NAMESPACE = "vault"

unseal_keys = [
    utils.get_env_var("VAULT_UNSEAL_KEY_1"),
    utils.get_env_var("VAULT_UNSEAL_KEY_2"),
    utils.get_env_var("VAULT_UNSEAL_KEY_3"),
]

def unseal_vault_pod(vault_pod):
    for key in unseal_keys:
        print(f"unsealing {vault_pod}")
        kubernetes_utils.run_kubectl_exec(
            vault_pod,
            VAULT_PODS_NAMESPACE,
            f"vault operator unseal {key}",
        )

def main():
    vault_pods = kubernetes_utils.run_kubectl_command(
        "get",
        "pods",
        VAULT_PODS_NAMESPACE,
        extra_flags=f"-l {VAULT_PODS_LABEL} -o jsonpath={{.items[*].metadata.name}}"
    ).split()

    with ThreadPoolExecutor(max_workers=len(vault_pods)) as executor:
        executor.map(unseal_vault_pod, vault_pods)

if __name__ == "__main__":
    main()
