# Scrap data on EVs from a gov. Website.

Write Python code to scrape data from
https://fame2.heavyindustries.gov.in/ModelUnderFame.aspx and store the
output in Excel.

<br>
When you open the site’s link, you will see a table of different EVs from a manufacturer.
There will be a total of 60 such manufacturers in that link. You need to scrape the data from all
of them.

## Column Definitions
- Manufacturer: For the manufacturer, you need to scrape the table headings
For example, Tata Motors Passenger Vehicles Limited (formerly known
as Tata Motors Limited), Kinetic Green Energy &amp; Power Solutions Ltd, etc.
- From column name “xEv model” name to column name “Status”, you
need to scrape it as it is, all the data.
- Links: In links columns, you need to scrape the links from the details field
of the site.
- JSON Data: In this column, you need to scrape the data from the link you
scraped in the links column, for example:
https://fame2.heavyindustries.gov.in/VehicleDetails.aspx?id=16. You need to scrape the data from all the links and store that in a JSON
format(use any format, but it should be in JSON).
