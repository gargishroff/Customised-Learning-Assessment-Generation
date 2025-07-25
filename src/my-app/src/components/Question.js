import { React } from "react";
import { Avatar, Typography, Card, Divider, Radio } from "antd";

const { Title, Text } = Typography;

function getAlphabet(index) {
  if (index < 0 || index >= 26) {
    throw new Error("Index out of range. Provide an index between 0 and 25.");
  }
  return String.fromCharCode(65 + index);
}

const AnswerSubjectiveBox = ({ ind, question_dict, setProp }) => {
  const { sample_answer } = question_dict;
  const setSampleAnswer = (e) => {
    setProp(ind, "sample_answer", e);
  };

  return (
    <>
      <Title level={5}>Sample Answer</Title>
      <Text editable={{ onChange: setSampleAnswer }}>{sample_answer}</Text>
    </>
  );
};

const MCQOptionBox = ({ ind, option_index, question_dict, setProp }) => {
  const { Meta } = Card;

  const { options, correct_answer } = question_dict;

  const setOptionAtIndex = (new_val) => {
    setProp(
      ind,
      "options",
      options.map((old_val, i) => {
        return i === option_index ? new_val : old_val;
      }),
    );
  };

  let card_style = {
    width: "100%",
    marginBottom: "10px",
    borderRadius: "8px",
    borderWidth: "2px",
  };
  if (option_index === correct_answer) {
    card_style.borderColor = "#1677ff";
  }
  return (
    <Card hoverable style={card_style}>
      <Meta
        style={{ float: "left" }}
        avatar={
          <Avatar style={{ backgroundColor: "#add8e6", color: "#000000" }}>
            {getAlphabet(option_index)}
          </Avatar>
        }
      />
      <Radio value={option_index}>
        <Text editable={{ onChange: setOptionAtIndex }}>
          {options[option_index]}
        </Text>
      </Radio>
    </Card>
  );
};

const AnswerMCQBox = ({ ind, question_dict, setProp }) => {
  const { options, correct_answer } = question_dict;
  const setCorrectAnswer = (e) => {
    setProp(ind, "correct_answer", e.target.value);
  };

  return (
    <>
      <Title level={5}>Options</Title>
      <Radio.Group
        size="large"
        onChange={setCorrectAnswer}
        value={correct_answer}
        style={{ display: "flex", flexDirection: "column" }}
      >
        {options.map((option, option_index) => (
          <MCQOptionBox
            ind={ind}
            option_index={option_index}
            question_dict={question_dict}
            setProp={setProp}
          />
        ))}
      </Radio.Group>
    </>
  );
};

const QuestionBox = ({ ind, question_dict, setProp }) => {
  const { question, question_type } = question_dict;
  const setQuestion = (e) => {
    setProp(ind, "question", e);
  };

  return (
    <Card
      hoverable
      title={`Question ${ind + 1}`}
      style={{
        width: "100%",
        marginBottom: "10px",
        borderRadius: "8px",
        borderWidth: "3px",
      }}
    >
      <Text editable={{ onChange: setQuestion }}>{question}</Text>
      <Divider />
      {question_type === "MCQ" ? (
        <AnswerMCQBox
          ind={ind}
          question_dict={question_dict}
          setProp={setProp}
        />
      ) : (
        <AnswerSubjectiveBox
          ind={ind}
          question_dict={question_dict}
          setProp={setProp}
        />
      )}
    </Card>
  );
};

export default QuestionBox;
