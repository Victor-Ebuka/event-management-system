import React, { useEffect, useState } from "react";
import axiosInstance from "../services/axiosConfig";
import { Link } from "react-router-dom";

const EventsPage = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await axiosInstance.get("events/");
        setEvents(response.data);
      } catch (err) {
        console.error("Error fetching events", err);
      }
    };
    fetchEvents();
  }, []);

  return (
    <div className="container mt-5">
      <h2>Your Events</h2>
      {events.length === 0 && <p>No events found. Start creating some!</p>}
      <div className="list-group">
        {events.map((event) => (
          <Link
            to={`/events/${event.id}`}
            key={event.id}
            className="list-group-item list-group-item-action"
          >
            {event.title}
          </Link>
        ))}
      </div>
    </div>
  );
};

export default EventsPage;
