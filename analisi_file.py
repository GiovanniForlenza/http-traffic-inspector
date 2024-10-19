import pyshark
import csv
from collections import defaultdict
import socket
from tqdm import tqdm

# Cache per memorizzare i risultati del reverse DNS lookup
domain_cache = {}

# Funzione per ottenere il dominio dall'IP tramite reverse DNS lookup
def get_domain_from_ip(ip):
    if ip in domain_cache:
        return domain_cache[ip]
    
    try:
        domain = socket.gethostbyaddr(ip)[0]  # Ricerca inversa DNS
    except socket.herror:
        domain = ip  # Se non riesce a risolvere il dominio, restituisce l'IP

    domain_cache[ip] = domain
    return domain

# Funzione per analizzare il file pcapng
def analyze_pcap(file_path):
    capture = pyshark.FileCapture(file_path, display_filter='http or quic or tcp.port == 443')

    results = defaultdict(lambda: {'http_requests': 0, 'http2_requests': 0, 'http3_requests': 0})

    # Ottieni il numero totale di pacchetti per mostrare il progresso
    total_packets = sum(1 for _ in capture)
    capture.reset()  # Resetta il capture per analizzarlo di nuovo

    with tqdm(total=total_packets, desc="Analizzando pacchetti", unit="pacchetto") as pbar:
        for packet in capture:
            domain = None
            try:
                # Verifica se è un pacchetto HTTP/1.x
                if 'http' in packet:
                    if hasattr(packet.http, 'host'):
                        domain = packet.http.host
                    elif hasattr(packet, 'ip'):
                        domain = get_domain_from_ip(packet.ip.dst)
                    results[domain]['http_requests'] += 1

                # Verifica se è un pacchetto HTTP/3 (QUIC)
                elif 'quic' in packet:
                    if hasattr(packet, 'ip'):
                        domain = get_domain_from_ip(packet.ip.dst)
                    results[domain]['http3_requests'] += 1

                # Verifica se è un pacchetto HTTPS/HTTP/2
                elif 'tcp' in packet and packet.tcp.dstport == '443':
                    if hasattr(packet, 'ip'):
                        domain = get_domain_from_ip(packet.ip.dst)
                    results[domain]['http2_requests'] += 1

            except AttributeError as e:
                print(f"Pacchetto ignorato: {e}")

            pbar.update(1)

    capture.close()
    return results

# Funzione per salvare i risultati in un file CSV
def save_results_to_csv(results, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sito', 'HTTP Requests', 'HTTP/2 Requests', 'HTTP/3 Requests'])
        for domain, counts in results.items():
            if domain:
                writer.writerow([domain, counts['http_requests'], counts['http2_requests'], counts['http3_requests']])

# Funzione principale
def main():
    pcap_file = "website_wireshark.pcapng"  # Specifica il tuo file .pcapng
    output_csv = "risultati_chiamate_http.csv"  # File CSV in cui salvare i risultati

    # Analizza il file pcap e ottieni i risultati
    results = analyze_pcap(pcap_file)

    # Salva i risultati in formato CSV
    save_results_to_csv(results, output_csv)

    print(f"Risultati salvati in {output_csv}")

if __name__ == "__main__":
    main()