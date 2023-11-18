import React, { useEffect, useState } from 'react';
import './Cluster.css';

function Cluster() {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [salaryInput, setSalaryInput] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 15; // Set the number of items per page

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_clusters');
      const result = await response.json();
      setData(result);
      setFilteredData(result);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleSalaryInputChange = (event) => {
    setSalaryInput(event.target.value);
  };

  const handleFilter = () => {
    const filtered = data.filter(item => item.SALARY === parseInt(salaryInput, 10));
    setFilteredData(filtered);
    setCurrentPage(1); // Reset to the first page when filtering
  };

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredData.slice(indexOfFirstItem, indexOfLastItem);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const Pagination = () => {
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);

    const handlePrevClick = () => {
      setCurrentPage((prevPage) => Math.max(prevPage - 1, 1));
    };

    const handleNextClick = () => {
      setCurrentPage((prevPage) => Math.min(prevPage + 1, totalPages));
    };

    return (
      <div className="pagination">
        <button onClick={handlePrevClick} disabled={currentPage === 1}>
          Previous
        </button>

        {Array.from({ length: totalPages }).map((_, index) => (
          <button
            key={index + 1}
            onClick={() => paginate(index + 1)}
            className={currentPage === index + 1 ? 'active' : ''}
          >
            {index + 1}
          </button>
        ))}

        <button onClick={handleNextClick} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
    );
  };

  return (
    <div className='content'>
      <div className='contain'>
        <label htmlFor="salaryInput">Enter Salary: </label>
        <input
          type="number"
          id="salaryInput"
          value={salaryInput}
          onChange={handleSalaryInputChange}
        />
        <button onClick={handleFilter}>Filter</button>
      </div>

      <div className='table-container'>
        <table className='feature'>
          <thead>
            <tr>
              <th>Name</th>
              <th>Salary</th>
            </tr>
          </thead>
          <tbody>
            {currentItems.map(item => (
              <tr key={item.NAMES}>
                <td>{item.NAMES}</td>
                <td>{item.SALARY}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Pagination />
    </div>
  );
}

export default Cluster;
