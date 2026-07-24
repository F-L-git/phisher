import netlas
import argparse
import cout
import inparse
import domain_mutations
import subdomains
import whoisreg


def main():
    # Main greeting
    print("\n")
    cout.print_banner()
    print("\n")

    # Processing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--perimeter", help="Path to file with perimeter data", required=True)
    parser.add_argument("-a", "--apikey", help="Personal Netlas API key", required=True)
    args = parser.parse_args()

    # Processing
    perimeter = inparse.Inparse()
    perimeter.parse(inparse.read(args.perimeter))
    # модулям передается готовый инициализированный Netlas объект
    netlas_connection = netlas.Netlas(api_key=args.apikey)

    potential_phishing = []

    mutations = domain_mutations.DomainMutations(netlas_connection)
    existing_mutdomains = mutations.search(domains=perimeter.domains)
    potential_phishing.extend(existing_mutdomains)

    SubdomainS = subdomains.Subdomains(netlas_connection)
    existing_subdomains = SubdomainS.search(names=perimeter.brandnames,
                                            legit_topdomains=perimeter.topdomains)
    potential_phishing.extend(existing_subdomains)

    registrant = whoisreg.WhoisIdentification(netlas_connection)
    correct_domains, wrong_domains = registrant.search(
        domains=potential_phishing, whois_data=perimeter.whois
    )
    
    potential_phishing = registrant.domain_double_check(
        true_links=perimeter.imglinks,
        keywords=perimeter.keywords,
        wrong_domains=wrong_domains
    )

    # Add correct domains
    if correct_domains:
        wrong_domains.update(correct_domains)

    # Print phishing domains
    print("\n")
    cout.print_domains(wrong_domains)


if __name__ == "__main__":
    main()
