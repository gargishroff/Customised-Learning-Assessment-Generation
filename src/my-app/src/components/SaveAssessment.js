import { React, useState } from "react";
import { Button, Tooltip, Modal, message } from "antd";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const SaveButton = ({ assessment, disabled }) => {
  const [modal_shown, setModalShown] = useState(false);
  const navigate = useNavigate();
  const saveAssessment = async (save_new_copy) => {
    let sent_assessment = { ...assessment };
    if (save_new_copy) {
      // id must not be sent for the backend to save in a new copy
      delete sent_assessment["_id"];
    }
    await axios
      .post("/save_assessment", sent_assessment, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        setModalShown(false);
        const new_id = response.data._id["$oid"];
        if (!new_id) {
          throw new Error("Did not get ID");
        }
        navigate(`/get_assessment/${new_id}`, {
          state: { last_modified: response.data.last_modified },
        });
      })
      .catch((error) => {
        console.error("Error saving Assessment: ", error);
        message.error("Failed to save assessment!");
      });
  };
  return (
    <Tooltip
      title={disabled ? "No changes made to save" : "Save current assessment"}
    >
      <Button
        type="primary"
        disabled={disabled}
        onClick={() => setModalShown(true)}
      >
        Save Assessment
      </Button>
      <Modal
        open={modal_shown}
        title="Saving the document"
        onOk={() => saveAssessment(true)}
        onCancel={() => setModalShown(false)}
        footer={[
          <Button onClick={() => setModalShown(false)}>
            Go back and not save
          </Button>,
          <Button danger type="primary" onClick={() => saveAssessment(false)}>
            Overwrite and save
          </Button>,
          <Button type="primary" onClick={() => saveAssessment(true)}>
            Copy and save
          </Button>,
        ]}
      >
        <p>
          You can choose to save your edits in a fresh copy, or overwrite the
          current assessment.
        </p>
        <p>
          Please note that if you pick to overwite the current assessment the
          old data will be permanently deleted.
        </p>
      </Modal>
    </Tooltip>
  );
};

export default SaveButton;
