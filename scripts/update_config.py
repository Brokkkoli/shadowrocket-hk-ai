"""Refresh official Voice addresses and publish the Hong Kong configuration."""
import ipaddress
import json
import os
from pathlib import Path
import re
import urllib.request

def render(template, data, repository):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Expected GitHub owner/repository")
    prefixes = []
    for entry in data["prefixes"]:
        keys = set(entry) & {"ipv4Prefix", "ipv6Prefix"}
        if len(keys) != 1:
            raise ValueError("Unexpected Voice address schema")
        network = ipaddress.ip_network(entry[next(iter(keys))], strict=True)
        if not network.is_global or network.num_addresses != 1:
            raise ValueError("Voice update contains a non-public or non-host prefix")
        prefixes.append(str(network))
    prefixes = sorted(set(prefixes), key=lambda value: (ipaddress.ip_network(value).version, int(ipaddress.ip_network(value).network_address)))
    if not 1 <= len(prefixes) <= 5000:
        raise ValueError("Unexpected Voice address count")
    voice = "# Official snapshot creationTime: " + str(data["creationTime"]) + "\n"
    voice += "\n".join(f"IP-CIDR,{prefix},PROXY,no-resolve" for prefix in prefixes)
    url = f"https://raw.githubusercontent.com/{repository}/main/Howard-HK-AI-Only.conf"
    result = template.replace("@@UPDATE_URL@@", url).replace("@@VOICE_RULES@@", voice)
    if "@@" in result or result.count("\nFINAL,DIRECT\n") != 1:
        raise ValueError("Invalid output template")
    if "FINAL,PROXY" in result or "dns-direct-fallback-proxy = true" in result:
        raise ValueError("Unexpected default routing")
    return result

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    repository = os.environ["GITHUB_REPOSITORY"]
    request = urllib.request.Request("https://openai.com/chatgpt-voice.json", headers={"User-Agent": "Shadowrocket-HK-AI-config-maintenance"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    output = render((root / "config.template.conf").read_text(), data, repository)
    destination = root / "Howard-HK-AI-Only.conf"
    temporary = destination.with_suffix(".tmp")
    temporary.write_text(output)
    temporary.replace(destination)
    print(f"Validated config generated: {len(data['prefixes'])} Voice addresses")
