IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'SystemEngineCore')
BEGIN
    CREATE DATABASE SystemEngineCore;
END
GO

USE SystemEngineCore;
GO

DROP TABLE IF EXISTS core.DataPersistenceStore;
DROP TABLE IF EXISTS core.SystemExecutionLogs;
DROP TABLE IF EXISTS core.UserProfiles;
DROP SCHEMA IF EXISTS core;
GO

CREATE SCHEMA core;
GO

CREATE TABLE core.UserProfiles (
    UserID INT IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL,
    AccessPinHash CHAR(64) NOT NULL,
    AccountCreatedDateTime DATETIME2 DEFAULT SYSUTCDATETIME(),
    IsActiveBit BIT DEFAULT 1,
    CONSTRAINT PK_UserProfiles PRIMARY KEY CLUSTERED (UserID),
    CONSTRAINT UQ_Username UNIQUE (Username)
);

CREATE TABLE core.DataPersistenceStore (
    DataRecordID INT IDENTITY(1,1),
    UserID INT NOT NULL,
    StringPayload NVARCHAR(MAX) NOT NULL,
    CommitTimestamp DATETIME2 DEFAULT SYSUTCDATETIME(),
    IsArchivedBit BIT DEFAULT 0,
    CONSTRAINT PK_DataPersistenceStore PRIMARY KEY CLUSTERED (DataRecordID),
    CONSTRAINT FK_DataPersistenceStore_UserProfiles FOREIGN KEY (UserID) 
        REFERENCES core.UserProfiles(UserID) ON DELETE CASCADE
);

CREATE TABLE core.SystemExecutionLogs (
    LogID BIGINT IDENTITY(1,1),
    ExecutionNode NVARCHAR(100) NOT NULL,
    LogSeverityLevel NVARCHAR(20) NOT NULL,
    MessageText NVARCHAR(500) NOT NULL,
    ExecutionTimeDeltaMS INT NOT NULL,
    LogTimestamp DATETIME2 DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_SystemExecutionLogs PRIMARY KEY CLUSTERED (LogID)
);
GO

CREATE NONCLUSTERED INDEX IX_DataPersistenceStore_User_Time
ON core.DataPersistenceStore (UserID, CommitTimestamp DESC)
INCLUDE (StringPayload);

CREATE NONCLUSTERED INDEX IX_SystemExecutionLogs_Severity_Node
ON core.SystemExecutionLogs (LogSeverityLevel, ExecutionNode)
INCLUDE (LogTimestamp);
GO

INSERT INTO core.UserProfiles (Username, AccessPinHash)
VALUES ('admin', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');

INSERT INTO core.DataPersistenceStore (UserID, StringPayload)
VALUES 
(1, 'Deploy primary Docker multi-stage build array successfully to remote server.'),
(1, 'Complete structural schema validation rules for backend SQL optimization run.');

INSERT INTO core.SystemExecutionLogs (ExecutionNode, LogSeverityLevel, MessageText, ExecutionTimeDeltaMS)
VALUES 
('Kivy_Callback_Async', 'INFO', 'System Lifecycle Tracker run initiated safely.', 12),
('Streamlit_Web_Core', 'WARNING', 'SQL Relational Load thread count approached threshold line.', 45);
GO

SELECT 
    u.Username,
    p.StringPayload,
    p.CommitTimestamp
FROM core.UserProfiles u
INNER JOIN core.DataPersistenceStore p ON u.UserID = p.UserID
WHERE u.IsActiveBit = 1
ORDER BY p.CommitTimestamp DESC;
