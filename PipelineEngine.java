package java_pipeline;

import java.util.ArrayList;
import java.util.List;

public class PipelineEngine {
    private final List<DataRecord> memoryBuffer;

    public PipelineEngine() {
        this.memoryBuffer = new ArrayList<>();
    }

    public void processStringData(int id, String rawPayload) {
        try {
            DataRecord record = new DataRecord(id, rawPayload);
            memoryBuffer.add(record);
            System.out.printf("[INFO] [Node: Java_Pipeline] Processed Record ID: %d at %s%n", 
                record.getRecordId(), record.getTimestamp());
        } catch (IllegalArgumentException e) {
            System.err.printf("[EXCEPTION] [Node: Java_Pipeline] Processing error on ID %d: %s%n", 
                id, e.getMessage());
        }
    }

    public List<DataRecord> getBuffer() {
        return new ArrayList<>(this.memoryBuffer);
    }

    public static void main(String[] args) {
        PipelineEngine engine = new PipelineEngine();
        
        engine.processStringData(101, "Deploy primary Docker multi-stage build array successfully.");
        engine.processStringData(102, "Complete structural schema validation rules for backend SQL optimization.");
        engine.processStringData(103, "   "); 
        
        System.out.printf("%n[INFO] Pipeline execution complete. Buffer retention size: %d records.%n", 
            engine.getBuffer().size());
    }
}
