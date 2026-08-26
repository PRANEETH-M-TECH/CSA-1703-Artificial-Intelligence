import axios from "axios";

const client = axios.create({ baseURL: "/api" });

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("taskmind_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default client;

export const AuthAPI = {
  signup: (data) => client.post("/auth/signup", data).then((r) => r.data),
  login: (data) => client.post("/auth/login", data).then((r) => r.data),
  me: () => client.get("/auth/me").then((r) => r.data),
  updateMe: (data) => client.put("/auth/me", data).then((r) => r.data),
};

export const TasksAPI = {
  list: () => client.get("/tasks").then((r) => r.data),
  create: (data) => client.post("/tasks", data).then((r) => r.data),
  update: (id, data) => client.put(`/tasks/${id}`, data).then((r) => r.data),
  remove: (id) => client.delete(`/tasks/${id}`).then((r) => r.data),
};

export const ScheduleAPI = {
  generate: () => client.post("/schedule/generate").then((r) => r.data),
  get: () => client.get("/schedule").then((r) => r.data),
};

export const ConflictsAPI = {
  check: () => client.post("/conflicts/check").then((r) => r.data),
  list: () => client.get("/conflicts").then((r) => r.data),
  explain: (id) => client.get(`/conflicts/${id}/explain`).then((r) => r.data),
  resolve: (id, action) => client.post(`/conflicts/${id}/resolve`, { action }).then((r) => r.data),
};

export const LearningAPI = {
  logHistory: (data) => client.post("/history", data).then((r) => r.data),
  train: () => client.post("/model/train").then((r) => r.data),
  recommendations: () => client.get("/recommendations").then((r) => r.data),
  acceptRecommendation: (category, best_hour) => client.post("/recommendations/accept", { category, best_hour }).then((r) => r.data),
  insights: () => client.get("/insights").then((r) => r.data),
};
