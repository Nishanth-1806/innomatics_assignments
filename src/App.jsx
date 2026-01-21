import React, { useState } from "react";

function App() {
  const [noteText, setNoteText] = useState("");
  const [notes, setNotes] = useState([]);

  const handleInputChange = (event) => {
    setNoteText(event.target.value);
  };

  const handleAddNote = () => {
    const trimmed = noteText.trim();
    if (!trimmed) return;

    setNotes((prevNotes) => [...prevNotes, trimmed]);
    setNoteText("");
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleAddNote();
    }
  };

  return (
    <div
      style={{
        maxWidth: "500px",
        margin: "2rem auto",
        fontFamily: "sans-serif",
        padding: "1rem",
        border: "1px solid #ddd",
        borderRadius: "8px",
      }}
    >
      <h1>Note Taking App</h1>

      <input
        type="text"
        placeholder="Type your note here..."
        value={noteText}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        style={{
          width: "100%",
          padding: "0.5rem",
          boxSizing: "border-box",
        }}
      />

      <button
        type="button"
        onClick={handleAddNote}
        style={{
          marginTop: "0.5rem",
          padding: "0.5rem 1rem",
          cursor: "pointer",
        }}
      >
        Add Note
      </button>

      <ul style={{ marginTop: "1rem" }}>
        {notes.map((note, index) => (
          <li key={index}>{note}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
