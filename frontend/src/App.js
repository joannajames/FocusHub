import { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import SpotList from "./components/SpotList";

const API_URL = "http://your-local-ip:8000/spots"; // Replace with actual IP

const App = () => {
  const [spots, setSpots] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => setSpots(data.spots))
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  const filteredSpots = spots.filter((spot) =>
    spot.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="max-w-2xl mx-auto p-6">
      <SearchBar setSearchQuery={setSearchQuery} />
      <SpotList spots={filteredSpots} />
    </div>
  );
};

export default App;
