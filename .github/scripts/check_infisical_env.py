"""Confere se as variáveis do .env.example existem e têm valor no Infisical.

Lê as pastas declaradas no infisical.yaml (já convertido para JSON), exporta cada
pasta em cada ambiente e compara só os nomes e se o valor está vazio. Nenhum valor
é impresso.

Ambientes:
- local: só aviso;
- qa: erro, se o repositório tiver a branch qa; sem a branch, é ignorado;
- prod: erro.
"""

import json
import os
import re
import subprocess
import sys

ENV_LINE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=")


def env_keys(path):
    keys = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            match = ENV_LINE.match(line)
            if match and match.group(1) not in keys:
                keys.append(match.group(1))
    return keys


def export_folder(env, folder, project, token):
    result = subprocess.run(
        [os.environ.get("INFISICAL_BIN", "infisical"), "export", f"--env={env}", f"--path={folder}", "--format=json",
         f"--projectId={project}", f"--token={token}", "--silent"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        return None
    try:
        return {item["key"]: bool(str(item.get("value", "")).strip()) for item in json.loads(result.stdout or "[]")}
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def main():
    config = json.loads(os.environ["INFISICAL_CONFIG"])
    folders = config.get("folders") or []
    ignore = set(config.get("ignore") or [])
    project = os.environ["INFISICAL_PROJECT_ID"]
    token = os.environ["INFISICAL_TOKEN"]
    has_qa = os.environ.get("HAS_QA_BRANCH") == "true"
    env_file = os.environ.get("ENV_FILE", ".env.example")

    if not folders:
        print("::error file=infisical.yaml::Nenhuma pasta declarada em folders.")
        return 1
    if not os.path.exists(env_file):
        print(f"::error::{env_file} não existe, mas o repositório declara pastas no infisical.yaml.")
        return 1

    keys = [key for key in env_keys(env_file) if key not in ignore]
    environments = [("local", "warning"), ("qa", "error" if has_qa else None), ("prod", "error")]
    summary = ["## Variáveis do Infisical", "", f"Pastas: {', '.join(folders)}", ""]
    summary.append("| Variável | local | qa | prod |")
    summary.append("|---|---|---|---|")
    status = {key: {} for key in keys}
    failed = False

    for env, level in environments:
        if level is None:
            for key in keys:
                status[key][env] = "sem branch qa"
            continue
        values = {}
        for folder in folders:
            exported = export_folder(env, folder, project, token)
            if exported is None:
                print(f"::{level}::Não foi possível ler a pasta {folder} no ambiente {env}.")
                failed = failed or level == "error"
                continue
            for key, has_value in exported.items():
                values[key] = values.get(key, False) or has_value
        for key in keys:
            if key not in values:
                status[key][env] = "ausente"
                print(f"::{level} file={env_file}::{key} não existe nas pastas declaradas no ambiente {env}.")
                failed = failed or level == "error"
            elif not values[key]:
                status[key][env] = "vazia"
                print(f"::{level} file={env_file}::{key} está vazia no ambiente {env}.")
                failed = failed or level == "error"
            else:
                status[key][env] = "ok"

    for key in keys:
        row = status[key]
        summary.append(f"| `{key}` | {row.get('local', '-')} | {row.get('qa', '-')} | {row.get('prod', '-')} |")
    if ignore:
        summary += ["", f"Ignoradas: {', '.join(sorted(ignore))}"]

    output = os.environ.get("GITHUB_STEP_SUMMARY")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write("\n".join(summary) + "\n")
    else:
        print("\n".join(summary))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
