rm srcForColor.zip
rm srcForMonitor.zip
cd srcForColor
zip -X -r ../srcForColor.zip *
cd ../srcForMonitor
zip -X -r ../srcForMonitor.zip *
cd ..
aws lambda update-function-code --function-name AskColor --zip-file fileb://srcForColor.zip
aws lambda update-function-code --function-name Monitor --zip-file fileb://srcForMonitor.zip
