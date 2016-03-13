rm src.zip
cd src
zip -X -r ../src.zip *
cd ..
aws lambda update-function-code --function-name AskColor --zip-file fileb://src.zip
