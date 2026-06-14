import axios from "axios";

export const predictRisk = async (latitude, longitude) => {
  const lat = Number(latitude.toFixed(2));
  const lng = Number(longitude.toFixed(2));

  const response = await axios.get(
    "/api/hydromet-service/predict-risk",
    {
      params: {
        latitude,
        longitude,
      },
    }
  );

  return response.data;
};