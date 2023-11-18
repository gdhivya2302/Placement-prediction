import React, { useState } from 'react';
import axios from 'axios';
import './Filter.css';
const Filter = () => {
  const [formData, setFormData] = useState({
    PYTHON: 0,
    JAVA: 0,
    DBMS: 0,
    'COMPUTER NETWORKS': 0,
    'MACHINE LEARNING': 0,
    'APTITUDE SKILLS': 0,
    'FULL STACK DEVELOPMENT': 0,
    'COMMUNICATION SKILLS': 0,
  });

  const [assignedSalary, setAssignedSalary] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: parseFloat(value) || 0, // Convert input to a float or default to 0
    });
  };

  const handleCalculateSalary = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/calculate_salary', formData);
      console.log(response.data.assigned_salary)
      setAssignedSalary(response.data.assigned_salary);
    } catch (error) {
      console.error('Error calculating salary:', error);
    }
  };

  return (
    <div>
      <center>
      <h1>Salary Calculator</h1></center>
      <form className='box'>
        {/* Input fields for each skill */}
        {Object.keys(formData).map((key) => (
          <div key={key} style={ {margin: '5px 0',
            padding:'8px'}}>
            <label htmlFor={key}>{key}</label>
            <input
              type="number"
              id={key}
              name={key}
              value={formData[key]}
              onChange={handleInputChange}
            />
          </div>
        ))}
        <button type="button" onClick={handleCalculateSalary} style={{width:'50%',marginLeft:'10%'}}>
          Calculate Salary
        </button>
        <br></br>
      </form>
      {assignedSalary !== null && (
        <center><h3>Assigned Salary: {assignedSalary}</h3></center>
      )}
    </div>
  );
};

export default Filter;