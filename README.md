# ocrmy-pdf-server

The excellent [OCRmyPDF](https://github.com/jbarlow83/OCRmyPDF) wrapped in a tiny web server that takes tasks per post requests.

```bash
docker run -d -p 8080:8080 choffmeister/ocrmypdf-server

curl -fsS -XPOST localhost:8080 --data-binary @input.pdf -o output.pdf
```
