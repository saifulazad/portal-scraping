const AWS = require('aws-sdk')
exports.upload = async (content) => {
  const dateString = new Date().toISOString().split('-')
  const year = dateString[0]
  const month = dateString[1]
  const day = dateString[2].split('T')[0]
  const params = {
    Bucket: 'extractor-service-dev/joblinksfile',
    Key: (`${year}-${month}-${day}`),
    Body: content.join('\r\n')
  }
  try {
    const uploadPromise = await new AWS.S3().putObject(params).promise()
    console.log('Successfully uploaded data to bucket')
  } catch (e) {
    console.log('Error uploading data: ', e)
  }
}
