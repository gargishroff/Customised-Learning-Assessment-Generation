import { UploadOutlined } from "@ant-design/icons";
import { Form, Input, Select, Button, Upload, message } from "antd";
import axios from "axios";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Loading from "../components/Loading";

axios.defaults.baseURL = "/api/v1";
axios.defaults.headers.common = { "Content-Type": "multipart/form-data" };

const { Option } = Select;

const MAX_FILE_UPLOADS = 3;

const MyForm = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [numfiles, setNumfiles] = useState(0);

  const onFinish = async (values) => {
    console.log("Form values:", values);
    setIsLoading(true);
    try {
      const formData = new FormData();
      values["pdfs"] = JSON.stringify(values["pdfs"]);
      for (const key in values) {
        if (values[key]) {
          formData.append(key, values[key]);
        }
      }

      const response = await axios.post("/generate_assessment", formData);
      console.log("Form submission successful:", response.data);
      setIsLoading(false);
      navigate(`/get_assessment/${response.data._id["$oid"]}`, {
        state: { response_data: response.data },
      });
    } catch (error) {
      console.error("Form submission failed:", error);
      let emsg = "Form submission failed: ";
      if (error.response) {
        if (
          error.response.status === 500 &&
          error.response.data.error === "llm"
        ) {
          emsg += "The backend LLM gave output in an incorrect format";
        } else {
          emsg += "Server error occurred";
        }
      } else {
        emsg += "Server didn't respond";
      }
      message.error(emsg);
      setIsLoading(false);
    }
  };

  const formStyle = {
    width: "75%", // Adjust the width as needed
    margin: "3% 0 auto", // Center the navbar by adding auto margin on left and right
  };

  const validateInteger = (rule, value) => {
    if (value && !/^[-+]?\d+$/.test(value)) {
      return Promise.reject();
    }
    return Promise.resolve();
  };

  const props = {
    beforeUpload: (file) => {
      if (numfiles >= MAX_FILE_UPLOADS) {
        message.error(
          `Cannot upload more than ${MAX_FILE_UPLOADS} files! You may remove a file that is already uploaded, to add a new file.`,
        );
        return Upload.LIST_IGNORE;
      }
      if (file.type !== "application/pdf") {
        message.error("You can only upload PDF files!");
        return Upload.LIST_IGNORE;
      }
      return true;
    },
    onRemove: (file) => {
      setNumfiles((prev_val) => prev_val - 1);
      return true;
    },
    onChange: (info) => {
      if (info.file.status === "done") {
        message.success(
          `${info.file.name} file uploaded successfully as ${info.file.response}`,
        );
        info.file.name = info.file.response;
      } else if (info.file.status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
      setNumfiles(info.fileList.length);
    },
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <>
      <Navbar></Navbar>
      <h1 style={{ textAlign: "center" }}>New Assessment</h1>
      <Form
        name="basic"
        labelCol={{ span: 8 }}
        wrapperCol={{ span: 16 }}
        onFinish={onFinish}
        style={formStyle}
      >
        {/* Topic Name */}
        <div
          style={{
            color: "grey",
            marginLeft: "33.5%",
            marginBottom: "0%",
            marginTop: "-1%",
          }}
        >
          Enter the main topic or subject of the Assessment to be Generated.
          (NOTE : The character limit is 125)
        </div>
        <Form.Item
          label="Topic"
          name="topic"
          style={{ marginBottom: "4%" }}
          rules={[
            {
              required: true,
              message: "Enter the Topic for Assesment Generation",
            },
            { max: 125, message: "Character limit exceeded" },
          ]}
        >
          <Input />
        </Form.Item>

        {/* Dropdown Menu (Type of Assessment)*/}
        <div
          style={{
            color: "grey",
            marginLeft: "33.5%",
            marginBottom: "0%",
            marginTop: "-1%",
          }}
        >
          Choose the type of questions required in the Assessment from the
          options provided.
        </div>

        <Form.Item
          label="Type of Assessment"
          name="question_type"
          style={{ marginBottom: "4%" }}
          rules={[{ required: true, message: "Please select an option!" }]}
        >
          <Select>
            <Option value="MCQs">MCQs</Option>
            <Option value="SA">Short Answers</Option>
            <Option value="LA">Long Answers</Option>
          </Select>
        </Form.Item>

        {/* Number of Questions */}
        <div
          style={{
            color: "grey",
            marginLeft: "33.5%",
            marginBottom: "0%",
            marginTop: "-1%",
          }}
        >
          Enter the number of questions in the Assessment (NOTE : The maximum
          limit is 20)
        </div>

        <Form.Item
          label="Number of Questions"
          name="num_questions"
          style={{ marginBottom: "4%" }}
          rules={[
            {
              required: true,
              message: "Please enter the number of questions!",
            },
            {
              validator: validateInteger,
              message: "Please enter a valid number of questions!",
            },
            {
              pattern: /^[1-9]$|^[1][0-9]$|^20$/,
              message: "Number of questions must be between 1 and 20!",
            },
          ]}
        >
          <Input type="number" />
        </Form.Item>

        <div
          style={{
            color: "grey",
            marginLeft: "33.5%",
            marginBottom: "0%",
            marginTop: "-1%",
          }}
        >
          In this field you can enter the contexual keywords i.e., specific
          concepts which are to be integrated with the main topic for Assessment
          Generation
        </div>
        <Form.Item
          label="Contextual Keywords"
          name="context_keywords"
          style={{ marginBottom: "4%" }}
        >
          <textarea
            style={{
              height: "200px",
              width: "100%",
              resize: "none",
              overflow: "hidden",
              whiteSpace: "pre-wrap",
              wordBreak: "break-all",
              overflowWrap: "break-word",
            }}
            wrap="soft"
          />
        </Form.Item>
        {/* PDF Upload Field */}
        <div
          style={{
            color: "grey",
            marginLeft: "33.5%",
            marginBottom: "0%",
            marginTop: "-1%",
          }}
        >
          You can upload file(s) for providing the content for Assessment
          Generation
        </div>
        <Form.Item label="Upload PDF" name="pdfs">
          <Upload
            {...props}
            action="/api/v1/upload_file"
            listType="picture"
            accept="application/pdf"
          >
            <Button icon={<UploadOutlined />}>Upload</Button>
          </Upload>
        </Form.Item>

        {/* Submit Button */}
        <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
    </>
  );
};

export default MyForm;
