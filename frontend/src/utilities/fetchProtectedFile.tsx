import apiClient from "./apiClient";

interface ErrorWithResponse {
    response?: {
        status: number;
    };
}

const fetchProtectedFile = async (filename:string) => {
    try {
        const formattedPath = filename.replace(/^\/?media\//, ""); 

        const response = await apiClient.get(`/protected-media/${formattedPath}/`, {
            responseType: "blob",
        });
        if (response.status === 200) {
            const blobUrl = URL.createObjectURL(response.data);
            if (blobUrl) {
                const link = document.createElement("a");
                link.href = blobUrl;
                link.setAttribute("download", filename.split("/").pop() || "download"); 
                document.body.appendChild(link);
                link.click();

                document.body.removeChild(link);
                URL.revokeObjectURL(blobUrl);
            }
        } else {
            console.error("Unauthorized or file not found");
        }
    } catch (error) {
        console.error("Error downloading file:", error);

        // Narrow the type of error
        if (error instanceof Error && error.message) {
            console.error("Error message:", error.message);
        }

        if (error && typeof error === "object" && "response" in error) {
            const response = (error as ErrorWithResponse).response;

            if (!response) {
                console.error("Network error or CORS issue – backend might be unreachable.");
                return;
            }

            if (response.status === 403) {
                console.error("You cannot access this file.");
                return;
            }
            if (response.status === 404) {
                console.error("File not found.");
                return;
            }
        }
    }
};


export default fetchProtectedFile;