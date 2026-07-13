package java_pipeline;

import java.time.Instant;

public class DataRecord {
    private final int recordId;
    private final String payload;
    private final Instant timestamp;

    public DataRecord(int recordId, String payload) {
        if (payload == null || payload.trim().isEmpty()) {
            throw new IllegalArgumentException("Payload validation failed: String cannot be empty.");
        }
        this.recordId = recordId;
        this.payload = payload;
        this.timestamp = Instant.now();
    }

    public int getRecordId() { return recordId; }
    public String getPayload() { return payload; }
    public Instant getTimestamp() { return timestamp; }
}
