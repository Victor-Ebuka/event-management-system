import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axiosInstance from "../services/axiosConfig";

const EventDetailsPage = () => {
  const { id } = useParams();
  const [event, setEvent] = useState(null);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const response = await axiosInstance.get(`events/${id}/`);
        setEvent(response.data);
      } catch (err) {
        console.error("Error fetching event details", err);
      }
    };
    fetchEvent();
  }, [id]);

  if (!event) return <p>Loading event details...</p>;

  return (
    <div className="container mt-5">
      <h2>{event.title}</h2>
      <p>{event.description}</p>
      <p>
        <strong>Date:</strong> {event.date}
      </p>
      <p>
        <strong>Time:</strong> {event.time}
      </p>
      <p>
        <strong>Location:</strong> {event.location}
      </p>
      {event.banner && <img src={event.banner} alt="Event Banner" />}
    </div>
  );
};

export default EventDetailsPage;
