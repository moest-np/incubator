const fs = require("fs");

function convertTSVtoCSV(inputFilePath, outputFilePath) {
  const tsvData = fs.readFileSync(inputFilePath, "utf8");

  const lines = tsvData.split("\n").filter((line) => line.trim() !== "");

  function removeQuotationMarks(str) {
    return str.replace(/"([^"]*)"/g, "$1");
  }

  const csvLines = lines.map((line) => {
    const remove = removeQuotationMarks(line);
    const values = remove.split("\t");
    const schoolId = `"${values[0]}"`;
    const school = `"${values[1]}"`;
    const velthuis = `"${values[2]}"`;
    const district1 = `"${values[3]}"`;
    const confidence = `"${values[4]}"`;
    const allMatches = `"${values[5]}"`;

    const csvLine = `${schoolId},${school},${velthuis},${district1},${confidence},${allMatches}`;

    return csvLine;
  });

  const csvData = csvLines.join("\n");

  fs.writeFileSync(outputFilePath, csvData, "utf8");

  console.log("Conversion completed. Output saved to " + outputFilePath);
}

const inputFilePath = "../data/school_list_A.tsv";
const outputFilePath = "school_list_A.csv";
convertTSVtoCSV(inputFilePath, outputFilePath);
