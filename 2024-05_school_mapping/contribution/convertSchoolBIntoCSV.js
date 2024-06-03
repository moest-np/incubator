const fs = require("fs");

function convertTSVtoCSV(inputFilePath, outputFilePath) {
  const tsvData = fs.readFileSync(inputFilePath, "utf8");
  const lines = tsvData.split("\n").filter((line) => line.trim() !== "");

  const csvLines = lines.map((line) => {
    const values = line.split("\t");
    const school_id = values[0];
    const name = values[1];
    const type = values[2];
    const status = values[3];
    const location = values[4];
    const ward = values[5];
    const local_level_id = values[6];
    const local_level = values[7];
    const district_id = values[8];
    const district = values[9];
    const province_id = values[10];
    const province = values[11];
    const old_name1 = values[12];
    const old_name2 = values[13];
    const old_name3 = values[14];

    const csvLine = `${school_id},${name},${type},${status},${location},${ward},${local_level_id},${local_level},${district_id},${district},${province_id},${province},${old_name1},${old_name2},${old_name3}`;

    return csvLine;
  });

  const csvData = csvLines.join("\n");
  fs.writeFileSync(outputFilePath, csvData, "utf8");
  console.log("Conversion completed. Output saved to " + outputFilePath);
}

const inputFilePath = "../data/school_list_B.tsv";
const outputFilePath = "../data/csv/school_list_B.csv";
convertTSVtoCSV(inputFilePath, outputFilePath);
