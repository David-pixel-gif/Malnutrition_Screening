import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar, ResponsiveContainer } from "recharts";
import Papa from "papaparse";

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [countryList, setCountryList] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState("ZIMBABWE");

  useEffect(() => {
    // Load CSV from public folder or static source
    fetch("/data/final_merged_malnutrition_data.csv")
      .then((response) => response.text())
      .then((csvText) => {
        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            const parsedData = results.data.map(row => ({
              ...row,
              Survey_Year: parseInt(row.Survey_Year),
              Stunting: parseFloat(row.Stunting),
              Wasting: parseFloat(row.Wasting),
              Overweight: parseFloat(row.Overweight),
              Underweight: parseFloat(row.Underweight)
            }));
            setData(parsedData);

            const uniqueCountries = [...new Set(parsedData.map(d => d.Country))].sort();
            setCountryList(uniqueCountries);
          },
        });
      });
  }, []);

  const filteredData = data.filter(d => d.Country === selectedCountry && !isNaN(d.Survey_Year));

  return (
    <div style={{ maxWidth: "1000px", margin: "auto", padding: "20px" }}>
      <h2>📊 Malnutrition Indicator Trends</h2>

      <label>Select Country:</label>
      <select
        value={selectedCountry}
        onChange={(e) => setSelectedCountry(e.target.value)}
        style={{ margin: "10px 0", padding: "5px" }}
      >
        {countryList.map((country) => (
          <option key={country} value={country}>
            {country}
          </option>
        ))}
      </select>

      <h3>Stunting, Wasting, Underweight & Overweight Over Time</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={filteredData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Survey_Year" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Stunting" stroke="#8884d8" name="Stunting" />
          <Line type="monotone" dataKey="Wasting" stroke="#82ca9d" name="Wasting" />
          <Line type="monotone" dataKey="Underweight" stroke="#ffc658" name="Underweight" />
          <Line type="monotone" dataKey="Overweight" stroke="#ff7300" name="Overweight" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Dashboard;