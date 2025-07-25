import React from "react";
import { Button } from "antd";
import { DownloadOutlined } from "@ant-design/icons";
import { saveAs } from "file-saver";
import { jsPDF } from "jspdf";

const ExportPdfButton = ({ assessment, fileName }) => {
  const { topic, num_questions, question_type, context_keywords, pdfs } =
    assessment.user_input;
  const { questions } = assessment;

  const exportPDF = () => {
    const docPDF = new jsPDF({
      orientation: "p",
      unit: "mm",
      format: "a4",
      putOnlyUsedFonts: true,
      margins: {
        top: 20,
        bottom: 20,
        left: 20,
        right: 20,
      },
    });

    let yPosition = 20; // Starting y position for content

    // Add heading to the PDF
    const heading = `Assessment Details:
    Topic: ${topic}
    Number of Questions: ${num_questions}
    Question Type: ${question_type}`;

    docPDF.setFontSize(12);
    docPDF.text(20, yPosition, heading);

    yPosition += docPDF.getTextDimensions(heading).h + 20; // Increase y position for next content

    // Add contextual keywords if available
    if (context_keywords) {
      const keywordsText = `Contextual Keywords: ${context_keywords}`;
      docPDF.setFontSize(12);
      docPDF.text(20, yPosition, keywordsText);
      yPosition += docPDF.getTextDimensions(keywordsText).h + 15; // Increase y position
    }

    // Add uploaded PDFs information if available
    if (pdfs && pdfs.length > 0) {
      const pdfsText = `Uploaded PDFs: ${pdfs.join(", ")}`;
      docPDF.setFontSize(12);
      docPDF.text(20, yPosition, pdfsText);
      yPosition += docPDF.getTextDimensions(pdfsText).h + 10; // Increase y position
    }

    // Add questions and answers to the PDF
    questions.forEach((question, index) => {
      const { question_type } = question;
      let content = `Question ${index + 1}: ${question.question}\n`;

      if (question_type !== "MCQ") {
        content += `Sample Answer: ${question.sample_answer}\n\n`;
      } else {
        question.options.forEach((option, i) => {
          content += `${String.fromCharCode(97 + i)}) ${option}\n`;
        });
        content += `Answer: ${String.fromCharCode(97 + question.correct_answer)}\n\n`;
      }

      // Check if adding this content exceeds current page height
      const textLines = docPDF.splitTextToSize(
        content,
        docPDF.internal.pageSize.width - 40,
      );
      const lineHeight = docPDF.getLineHeight() / docPDF.internal.scaleFactor;
      const requiredHeight = textLines.length * lineHeight;

      if (yPosition + requiredHeight > docPDF.internal.pageSize.height - 20) {
        // Add new page
        docPDF.addPage();
        yPosition = 20; // Reset y position for new page
      }

      // Add content to PDF
      docPDF.text(20, yPosition, textLines);
      yPosition += requiredHeight + 10; // Increase y position for next content
    });

    // Save the PDF as a Blob
    const pdfBlob = docPDF.output("blob");
    saveAs(pdfBlob, fileName);
  };

  const buttonStyle = {
    marginBottom: "3%",
    marginTop: "0.5%",
  };

  return (
    <div style={buttonStyle}>
      <Button
        type="primary"
        icon={<DownloadOutlined />}
        onClick={exportPDF}
        style={buttonStyle}
      >
        Export to PDF
      </Button>
    </div>
  );
};

export default ExportPdfButton;
