import axios from "axios";

const token = localStorage.getItem("token");

const api = axios.create({
  baseURL: "http://localhost:3002/api/invoices",
  responseType: "json",
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

export const getCampaigns = () => api.get("/campaigns");

export const getCampaign = ({ campaignId }) =>
  api.get(`/campaigns/${campaignId}`);

export const getLineItems = (params) => api.get("/line-items", { params });

export const getLineItem = ({ lineItemId }) =>
  api.get(`/line-items/${lineItemId}`);

export const patchLineItem = ({ lineItemId, lineItemEditPayload }) =>
  api.patch(`/line-items/${lineItemId}`, lineItemEditPayload);
