import {
  message,
  Popconfirm,
  Select,
  Input,
  Spin,
  Empty,
  Typography,
  Card,
  Pagination,
} from "antd";
import axios from "axios";
import React, { useState, useEffect } from "react";
import { FaTrash } from "react-icons/fa";
import { useLocation, useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";

const { Option } = Select;
const { Search } = Input;
const { Title, Text } = Typography;

const HistoryPage = () => {
  const location = useLocation();
  const [historyData, setHistoryData] = useState(null);
  const [originalData, setOriginalData] = useState(null);
  const [sortOrder, setSortOrder] = useState("recentToOldest");
  const [searchKeyword, setSearchKeyword] = useState("");
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  // load all assessment dictionaries from backend.
  useEffect(() => {
    setLoading(true);
    axios
      .get(location.pathname)
      .then((response) => {
        setLoading(false);
        if (response.headers["content-type"] !== "application/json") {
          throw new Error("Did not get JSON data");
        }
        setHistoryData(response.data);
        setOriginalData(response.data);
      })
      .catch((error) => {
        setLoading(false);
        console.error("Error fetching history: ", error);
        message.error("Failed to load history data!");
      });
  }, [location.pathname]);

  useEffect(() => {
    if (originalData) {
      // Ensure original data is available
      let sortedData = [...originalData]; // Use original data for sorting and filtering
      if (sortOrder === "recentToOldest") {
        sortedData = sortedData.sort(
          (a, b) => new Date(b.last_modified) - new Date(a.last_modified),
        );
      } else if (sortOrder === "oldestToRecent") {
        sortedData = sortedData.sort(
          (a, b) => new Date(a.last_modified) - new Date(b.last_modified),
        );
      }
      const filteredData = sortedData.filter((assessment) =>
        assessment.user_input.topic
          .toLowerCase()
          .includes(searchKeyword.toLowerCase()),
      );
      setHistoryData(filteredData);
    }
  }, [sortOrder, searchKeyword, originalData]);

  const navigate = useNavigate();
  const handleAssessmentClick = (assessmentId) => {
    navigate(`/get_assessment/${assessmentId["$oid"]}`);
  };

  const handleDeleteAssessment = (assessmentId) => {
    axios
      .delete(`/delete_assessment/${assessmentId["$oid"]}`)
      .then((response) => {
        message.success(response.data.message);
        setOriginalData((prevData) =>
          prevData.filter((assessment) => assessment._id !== assessmentId),
        );
        setHistoryData((prevData) =>
          prevData.filter((assessment) => assessment._id !== assessmentId),
        );
      })
      .catch((error) => {
        console.error("Error deleting assessment: ", error);
        message.error("Failed to delete assessment!");
      });
  };

  const handleSortOrderChange = (value) => {
    setSortOrder(value);
  };

  const handleSearch = (value) => {
    setSearchKeyword(value.trim());
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const handlePageSizeChange = (current, value) => {
    setPageSize(value);
    setCurrentPage(current); // Reset to first page when changing page size
  };

  const paginatedData =
    historyData &&
    historyData.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  return (
    <>
      <Navbar />
      <div style={{ padding: "20px" }}>
        <Title level={2} style={{ textAlign: "center", marginBottom: "20px" }}>
          List of Already Generated Assessments
        </Title>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "20px",
          }}
        >
          <Select
            defaultValue="recentToOldest"
            style={{ width: 200 }}
            onChange={handleSortOrderChange}
          >
            <Option value="recentToOldest">Sort: From Recent to Oldest</Option>
            <Option value="oldestToRecent">Sort: Oldest to Recent</Option>
          </Select>
          <Search
            placeholder="Search by topic"
            onSearch={handleSearch}
            enterButton
            style={{ width: 300 }}
          />
        </div>
        {loading ? (
          <Spin size="large" />
        ) : (
          <>
            {historyData && historyData.length > 0 ? (
              <>
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns:
                      "repeat(auto-fill, minmax(300px, 1fr))",
                    gap: "20px",
                  }}
                >
                  {paginatedData.map((assessment, index) => (
                    <Card
                      key={`history-item-${index}`}
                      hoverable
                      style={{ width: 300, margin: "0 0 20px 0" }}
                      onClick={() => handleAssessmentClick(assessment._id)}
                    >
                      <div>
                        <Title level={4}>
                          Assessment on {assessment.user_input.topic}
                        </Title>
                        <Text strong>Last modified:</Text>{" "}
                        <Text>{assessment.last_modified}</Text>
                        <br /> {/* New line here */}
                        <Text strong>Question Type:</Text>{" "}
                        <Text>{assessment.user_input.question_type}</Text>
                      </div>
                      <div onClick={(e) => e.stopPropagation()}>
                        <Popconfirm
                          title="Are you sure you want to delete this assessment?"
                          onConfirm={() =>
                            handleDeleteAssessment(assessment._id)
                          }
                          okText="Yes"
                          cancelText="No"
                        >
                          <FaTrash style={styles.trashIcon} />
                        </Popconfirm>
                      </div>
                    </Card>
                  ))}
                </div>
                <Pagination
                  style={{ textAlign: "center", marginTop: "20px" }}
                  current={currentPage}
                  pageSize={pageSize}
                  total={historyData.length}
                  onChange={handlePageChange}
                  onShowSizeChange={(current, size) =>
                    handlePageSizeChange(current, size)
                  }
                />
              </>
            ) : (
              <Empty />
            )}
          </>
        )}
      </div>
    </>
  );
};

const styles = {
  trashIcon: {
    color: "grey",
    cursor: "pointer",
    position: "absolute",
    top: "5px",
    right: "5px",
  },
};

export default HistoryPage;
