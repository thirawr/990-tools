# 990 Tools Outline

## EFILE Export v1
- This is an app within the 990 Tools Django project
- Provides a web interface to allow users to select a set of organizations and fields to export as CSV


### Views

#### Forms
- The primary view on this app will be a series of forms that allow a user to specify criteria before downloading a CSV generated based on that criteria


1. Specify a set of `tax years` or `fiscal years`
2. Choose a set of `organizations` you'd like to export
3. Select a set of fields (`db_name`) < form parts (`parent_sked_part`) < schedules (`parent_sked`)* that you'd like to export
  - The carats indicate the granularity of each variable type
  - Ideally I'd like to be able to pull down an accordion from the top down to increase/decrease field granularity
  - I select Schedule J and it automatically selects all fields within Schedule J, but then I open the Schedule J accordion and I can de-select some fields that have been checked
  - Some fields will not be able to be de-selected: All reports will generate with identifier and TY/FY information


- These forms will all be populated by choices currently available in the 990 XML database
- I.E., if Foo Organization hasn't filed for TY16 and you request TY16 forms, Foo Organization will not show up in your org selection form
- ya dig?

#### CSV Stream
- This endpoint will compile the requested CSV and stream it


### Models/Databases

#### EFILE Metadata
- Managed? by Django - data hosted in [repo submodule](https://github.com/jsfenfen/990-xml-metadata)
  - We'll have command management scripts for updating these models with new versions
- Database representation of canonicalized EFILE fields
- User-friendly names for schedules and form parts (lookup tables)
- We will use these field lists to map between the user-friendly field list in the forms and the database field names
- The EFILE metadata should be updated concurrently when we update the `990-xml-database`
  - _These two need to be version locked together or it will not be pretty_

#### Return
- Not managed by Django
- This is the `990-xml-database` and we will use Django tools to generate models based on the current state of the db
  - These models will need to be updated if the database schema changes going forward
- the field value `db_name` in `variables` in the efile metadata will correspond to property names for each model, which will correspond to a `db_table` in `variables`
- We can `getattr(modelInstance, specifiedFormDBName)` to compile a 990 report


### Challenges
- This app should be flexible enough to handle schema changes to the 990 database
- 990 Tools does not manage the 990 database; thus, we should avoid hardcoding wherever possible in this project
- We need to rely on the model representation of the EFILE schema to identify database field names
- The established database schema is not likely to change _significantly_ because the schema has been canonicalized, but it's important to note that things _could_ change as the EFILE schema changes with revisions to the U.S. Tax Code.
- Let's not build a nightmare...
- Our version of the 990 XML metadata differs from the [upstream version](https://github.com/jsfenfen/990-xml-metadata) on two fields:
  - On PF Part VI, `db_name` `AppldTESTxAmt` has been renamed to `AppldTCrdtNxtYr` to resolve a duplicate column name issue (`AppldTEsTxAmt`)
    - This is not an issue in PostgreSQL because the columns are case-sensitive
  - On `SkdASpprtdOrgInfrmtn`, `EIN` has been renamed to `SpprtdOrgEIN` to resolve a similar duplicate column name issue
  - We have a [pending issue](https://github.com/jsfenfen/990-xml-metadata/issues/2#issuecomment-395192434) on the repo, but if Jacob doesn't want to merge our custom fields we can always write band-aid code when updating the schema tables
