# manf #

Run server.py to start the flask web server on localhost. An internet connection is required so the server can fetch data from an external database server (although the db location can be changed in code).

### What is manf for? ###

* Catalogue of electronic components, storing key information for design such as footprints, environmental compliance, market data etc.
* Allows engineers to find suitable parts from manf to use in a design, and easily move into a BoM with support for build variants, not fit parts, second source supplier etc.
* Allows custom comments/specs/parameters to be associated with parts, such as suitability for a design, previous problems, soldering issues etc. As well as mark certain parts as end of life.

### List of Features ###

Parts
 * Parameters/Specs
 * Market Data (Price/Availability)
 * Status (unapproved, end of life, long lead etc)
 * Alternative parts/second sourcing
 * Stock levels/location
Boms
 * Bom storage, parts linked to parts in DB
 * Bom variants
 * Bom to bom comparison
 * Compliance checking (RoHS/Reach etc)
 * MTBF maybe?
Users
 * Authentication from google login
 * Tierd access for part creation/approval/settings control
 * ...