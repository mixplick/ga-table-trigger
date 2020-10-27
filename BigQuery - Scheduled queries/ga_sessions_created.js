const {
    BigQuery
} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

exports.extractReport = async (req, res) => {
    
    //Create insert query
    const query = `INSERT INTO
            \`PROJECT-ID.DATASET.TABLE\` ...`;

    // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
    const options = {
        query: query,
        // Location must match that of the dataset(s) referenced in the query.
        location: 'US',
        //destination: destinationTable,
    };

    // Run the query as a job
    const [job] = await bigquery.createQueryJob(options);
}
// [END bigquery_query_destination_table]
