import { useState, useEffect } from react;

// 🌱 Example Data Flow

// User completes session.

// React:

// Calls POST /complete-session

// Backend:

// Increments streak

// Adds session record

// Returns updated stats

// React:

// Updates streak in UI

// Triggers animation

// Updates garden display

// That’s real client-server architecture.