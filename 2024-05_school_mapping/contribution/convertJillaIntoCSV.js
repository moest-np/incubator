const fs = require("fs");

function convertTSVtoCSV(inputFilePath, outputFilePath) {
  const tsvData = fs.readFileSync(inputFilePath, "utf8");

  const lines = tsvData.split("\n").filter((line) => line.trim() !== "");

  const csvLines = lines.map((line) => {
    const values = line.split("\t");
    const district_id = values[0];
    const district = values[1];
    const जिल्ला = values[2];

    const csvLine = `${district_id},${district},${जिल्ला}`;

    return csvLine;
  });

  const csvData = csvLines.join("\n");

  fs.writeFileSync(outputFilePath, csvData, "utf8");

  console.log("Conversion completed. Output saved to " + outputFilePath);
}

const inputFilePath = "../data/jilla.tsv";
const outputFilePath = "../data/csv/jilla.csv";
convertTSVtoCSV(inputFilePath, outputFilePath);
