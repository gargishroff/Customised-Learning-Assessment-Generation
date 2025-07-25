import React from "react";
import { Button } from "antd";
import { DownloadOutlined } from "@ant-design/icons";
import { saveAs } from "file-saver";
import { Packer, Document, Paragraph, TextRun, HeadingLevel } from "docx";

function generateParagraphs(questionDict) {
  const paragraphs = [];

  for (let index = 0; index < questionDict.length; index++) {
    const element = questionDict[index];

    // Create paragraph for the question
    paragraphs.push(
      new Paragraph({
        children: [
          new TextRun({
            text: "Question " + (index + 1) + ": " + element["question"],
            bold: true,
            size: 24,
          }),
        ],
        spacing: {
          before: 200, // Add spacing before each question
          after: 100, // Add spacing after each question
        },
      }),
    );

    // Check question type
    if (element["question_type"] !== "MCQ") {
      // Create paragraph for sample answer
      paragraphs.push(
        new Paragraph({
          children: [
            new TextRun({
              text: "Sample Answer: " + element["sample_answer"],
              bold: false,
              size: 22,
            }),
          ],
          spacing: {
            after: 200, // Add spacing after sample answer
          },
        }),
      );
    } else {
      // Add options for MCQ questions
      const options = element["options"];
      for (let i = 0; i < options.length; i++) {
        paragraphs.push(
          new Paragraph({
            children: [
              new TextRun({
                text: String.fromCharCode(97 + i) + ") " + options[i],
                bold: false,
                size: 22,
              }),
            ],
          }),
        );
      }

      // Create paragraph for correct answer
      paragraphs.push(
        new Paragraph({
          children: [
            new TextRun({
              text:
                "Answer: " +
                String.fromCharCode(97 + element["correct_answer"]),
              bold: true,
              size: 22,
            }),
          ],
          spacing: {
            after: 200, // Add spacing after the answer
          },
        }),
      );
    }

    // Add additional space between questions
    if (index < questionDict.length - 1) {
      paragraphs.push(
        new Paragraph({
          children: [
            new TextRun({
              text: "", // Empty line for spacing
              size: 11,
            }),
          ],
          spacing: {
            after: 200, // Add spacing after each question block
          },
        }),
      );
    }
  }

  return paragraphs;
}

function generateHeadings(assessment) {
  // Create a header with the specified topic
  const { topic, num_questions, question_type, context_keywords, pdfs } =
    assessment;
  var head = `The below assessment has ${num_questions} ${question_type} question(s) on the topic '${topic}'`;
  const header = [
    new Paragraph({
      children: [
        new TextRun({
          text: head,
          // bold: true,
          size: 48, // Adjust the font size as needed
        }),
      ],
      // alignment: "center", // Center align the text in the header
    }),
  ];
  if (context_keywords) {
    // head += `in reference to these contextual keywords: ${context_keywords}`
    header.push(
      new Paragraph({
        children: [
          new TextRun({
            text: `In reference to these contextual keywords: ${context_keywords}`,
            size: 40,
          }),
        ],
      }),
    );
  }
  if (pdfs && pdfs.length > 0) {
    // head+="\nThe pdfs uploaded are: "
    var pdf = "The uploaded pdfs are: ";
    pdfs.forEach((element) => {
      pdf += `${element}, `;
    });
    head -= ", ";
    header.push(
      new Paragraph({
        children: [
          new TextRun({
            text: pdf,
            headings: HeadingLevel.HEADING_2,
          }),
        ],
      }),
    );
  }

  // Return the list of header components
  return header;
}

const ExportDocxButton = ({ assessment, fileName }) => {
  const exportDocx = async () => {
    const headings = generateHeadings(assessment.user_input);
    const paragraphs = generateParagraphs(assessment.questions);

    // Concatenate headings and paragraphs
    const content = headings.concat(paragraphs);
    const doc = new Document({
      sections: [
        {
          properties: {},
          children: content,
        },
      ],
    });

    Packer.toBlob(doc).then((blob) => {
      saveAs(blob, fileName);
    });
  };

  const buttonStyle = {
    marginBottom: "3%", // Adjust margin as needed
    marginTop: "0.5%",
  };

  return (
    <div style={buttonStyle}>
      <Button
        type="primary"
        icon={<DownloadOutlined />}
        onClick={exportDocx}
        style={buttonStyle}
      >
        Export to DOCX
      </Button>
    </div>
  );
};

export default ExportDocxButton;
