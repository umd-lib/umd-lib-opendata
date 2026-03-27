---
title: APIs
---

Introduction to various Application Programming Interfaces (API) (and metadata
formats) available for dynamic query of our services.

## OAI-PMH

From the [OAI-PMH](https://www.openarchives.org/pmh/) home page:

> The Open Archives Initiative Protocol for Metadata Harvesting (OAI-PMH)
> is a low-barrier mechanism for repository interoperability. Data Providers are
> repositories that expose structured metadata via OAI-PMH. Service Providers then
> make OAI-PMH service requests to harvest that metadata. OAI-PMH is a set of six verbs
> or services that are invoked within HTTP.

For more information see <https://www.openarchives.org/pmh/>.

## OpenSearch

From the [OpenSearch](https://en.wikipedia.org/wiki/OpenSearch_(specification)) Wikipedia
entry:

> OpenSearch is a collection of technologies that allow publishing of search
> results in a format suitable for syndication and aggregation. It is a way
> for websites and search engines to publish search results in a standard and
> accessible format.

For more information see the [OpenSearch
specification](https://github.com/dewitt/opensearch).

## DSpace REST API

DSpace REST API, first introduced in DSpace version 7. For more information see
[REST Contract /
Documentation](https://github.com/DSpace/RestContract/blob/main/README.md).
This contract provides detailed information on how to interact with the API,
what endpoints are available, etc. All features/capabilities of the DSpace UI
are available in this API.

## OpenAPI Specification {#open-api}

The [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (OAS)
defines a standard, programming language-agnostic interface description for
HTTP APIs, which allows both humans and computers to discover and understand
the capabilities of a service without requiring access to source code,
additional documentation, or inspection of network traffic. When properly
defined via OpenAPI, a consumer can understand and interact with the remote
service with a minimal amount of implementation logic. Similar to what
interface descriptions have done for lower-level programming, the OpenAPI
Specification removes guesswork in calling a service.

## Search/Retrieve via URL (SRU) {#sru}

From the [Search/Retrieve via URL](https://en.wikipedia.org/wiki/Search/Retrieve_via_URL)
Wikipedia entry:

> Search/Retrieve via URL (SRU) is a standard search protocol for Internet
> search queries, utilizing Contextual Query Language (CQL), a standard query
> syntax for representing queries.
>

From the [Library of Congress SRU](https://www.loc.gov/standards/sru/) home page:

> Search/Retrieve via URL (SRU) is a standard for searching and retrieving
> information from remote information services. It is based on the Z39.50
> protocol, but uses HTTP as the transport mechanism and XML as the encoding
> format.

## JSON-LD {#json-ld}

From the [JSON-LD](https://en.wikipedia.org/wiki/JSON-LD) Wikipedia entry:

> JSON-LD (JavaScript Object Notation for Linked Data) is a method of encoding
> linked data using JSON and of serializing data similarly to traditional JSON.
> It is meant to be simple to create by modifying JSON documents. JSON-LD is a
> World Wide Web Consortium Recommendation initially developed by the JSON for
> Linking Data Community Group, transferred to the RDF Working Group for review,
> improvement and standardization, and now maintained by the JSON-LD Working
> Group.

JSON-LD can be served as a standalone JSON-LD document or embedded in HTML,
commonly as [schema.org](https://schema.org/) structured data.  See
[Introduction to structured data markup in Google
Search](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data?hl=en)
for information on embedding JSON-LD as structured data.
