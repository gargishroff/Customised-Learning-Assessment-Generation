import { message } from "antd";
import axios from "axios";
import { React, useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

import Navbar from "../components/Navbar";
import Loading from "../components/Loading";
import QuestionBox from "../components/Question";
import ExportDocxButton from "../components/ExportDocxButton";
import ExportPdfButton from "../components/ExportPdfButton";
import SaveButton from "../components/SaveAssessment";

const AssessmentDisplay = () => {
  const location = useLocation();
  const [assessment, setAssessment] = useState(location.state?.response_data);
  const [made_edits, setMadeEdits] = useState(false);
  const setQuestionProp = (i, key, value) => {
    const new_data = { ...assessment };
    if (new_data.questions[i][key] !== value) {
      new_data.questions[i][key] = value;
      setAssessment(new_data);
      setMadeEdits(true);
    }
  };

  const ConfirmationPrompt = () => {
    // This component implements the confirmation prompt displayed when the
    // user tries to leave the page with unsaved edits.
    useEffect(() => {
      const handleBeforeUnloadConfirmation = (e) => {
        if (made_edits) {
          const confirmationMessage =
            "Are you sure you want to leave this page?";
          e.returnValue = confirmationMessage; // For older browsers
          return confirmationMessage; // For modern browsers
        }
      };

      if (made_edits) {
        window.addEventListener("beforeunload", handleBeforeUnloadConfirmation);
      }

      return () => {
        window.removeEventListener(
          "beforeunload",
          handleBeforeUnloadConfirmation,
        );
      };
    });

    return null; // This component doesn't render anything visible
  };

  /*
    Fetch assessment from backend if:
    1) It is not available.
    2) The wrong assessment is currently loaded.
    3) A newer revision of the assessment is available.
  */
  if (
    !assessment ||
    assessment._id["$oid"] !== location.pathname.split("/").pop() ||
    (location.state?.last_modified &&
      location.state?.last_modified !== assessment.last_modified)
  ) {
    axios
      .get(location.pathname)
      .then((response) => {
        if (response.headers["content-type"] !== "application/json") {
          throw new Error("Did not get json data");
        }
        setAssessment(response.data);
        setMadeEdits(false);
      })
      .catch((error) => {
        console.error("Error saving assessment: ", error);
        message.error("Failed to load assessment!");
      });
  }

  if (!assessment) {
    // display loading UI when the assessment is being loaded.
    return <Loading />;
  }

  const { topic, question_type, num_questions, context_keywords, pdfs } =
    assessment.user_input || {};

  return (
    <>
      <Navbar />

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "100vh",
        }}
      >
        <div style={{ width: "80%", maxWidth: "800px" }}>
          <div id="contentToExport">
            <div class="prompt-container" style={styles.promptContainer}>
              <p>
                <b>
                  The below assessment has {num_questions} {question_type}{" "}
                  question(s) on the topic '{topic}'.<br></br>
                  {context_keywords ? (
                    <>Context keywords: {context_keywords}.</>
                  ) : (
                    <>No context keywords were supplied.</>
                  )}
                  <br></br>
                  {pdfs && pdfs.length > 0 ? (
                    <>
                      Using contexts from the following uploaded PDF files -{" "}
                      <ul>
                        {pdfs.map((item, index) => (
                          <li>{item}</li>
                        ))}
                      </ul>
                    </>
                  ) : (
                    <>No context PDF files were uploaded.</>
                  )}
                </b>
              </p>
            </div>

            <h2>Assessment Questions</h2>
            {assessment.questions && assessment.questions.length > 0 ? (
              assessment.questions.map((item, index) => (
                <QuestionBox
                  ind={index}
                  question_dict={item}
                  setProp={setQuestionProp}
                />
              ))
            ) : (
              <p>No assessment questions to display.</p>
            )}
          </div>
        </div>
        <div style={styles.buttonContainer}>
          <ExportPdfButton assessment={assessment} fileName="assessment" />
          <ExportDocxButton assessment={assessment} fileName="assessment" />
          <SaveButton assessment={assessment} disabled={!made_edits} />
        </div>
        <ConfirmationPrompt />
      </div>
    </>
  );
};

const styles = {
  promptContainer: {
    backgroundColor: "rgba(173, 216, 230, 0.3)",
    padding: "10px",
    borderRadius: "5px",
    margin: "2% 0%",
    border: "2px solid black",
  },
  buttonContainer: {
    display: "flex",
    justifyContent: "center",
    marginTop: "20px",
    gap: "20px",
  },
};

export default AssessmentDisplay;
