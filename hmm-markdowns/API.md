# Cypher API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently no authentication required. Future versions will implement JWT tokens.

## Endpoints

### 1. Health Check
Check if the API server is running.

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "Cypher API",
  "version": "1.0.1"
}
```

**Status Codes**:
- `200 OK`: Server is healthy

---

### 2. Fetch Results
Fetch student results from the university portal.

**Endpoint**: `POST /api/fetch-results`

**Request Body**:
```json
{
  "hallTicket": "YOUR_HALL_TICKET",
  "examType": "general",
  "viewType": "All Semesters"
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| hallTicket | string | Yes | Student hall ticket number |
| examType | string | No | Type of exam (general, honors, minors) |
| viewType | string | No | View type (All Semesters, Single Semester) |

**Success Response** (200 OK):
```json
{
  "studentInfo": {
    "hallTicket": "YOUR_HALL_TICKET",
    "name": "STUDENT NAME",
    "program": "B TECH in COMPUTER SCIENCE"
  },
  "subjects": [
    {
      "code": "CS101",
      "name": "Data Structures",
      "credits": "3.00",
      "grade": "A",
      "marks": "85"
    }
  ],
  "semesterInfo": {
    "gpa": 8.5,
    "semester": 3
  },
  "analytics": {
    "gpa": 8.5,
    "performanceLevel": "Excellent",
    "totalSubjects": 10,
    "passFailStatus": {
      "passed": 10,
      "failed": 0,
      "overallStatus": "Pass",
      "failedSubjects": []
    },
    "gradeDistribution": {
      "A": 3,
      "B": 5,
      "C": 2
    }
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid input
```json
{
  "error": "Hall ticket number is required"
}
```

- `404 Not Found`: Results not found
```json
{
  "error": "Failed to retrieve results. Please check hall ticket."
}
```

- `500 Internal Server Error`: Server error
```json
{
  "error": "Internal server error: <details>"
}
```

---

### 3. Export Results
Export results to CSV or Excel format.

**Endpoint**: `POST /api/export`

**Request Body**:
```json
{
  "data": {
    "studentInfo": { ... },
    "subjects": [ ... ],
    "analytics": { ... }
  },
  "format": "csv"
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data | object | Yes | Complete results data object |
| format | string | No | Export format: "csv" or "excel" (default: csv) |

**Success Response** (200 OK):
- Returns file download with appropriate Content-Type
- Filename: `results_{hallTicket}_{timestamp}.{format}`

**Status Codes**:
- `200 OK`: File generated successfully
- `400 Bad Request`: No data provided
- `500 Internal Server Error`: Export failed

---

## Data Models

### StudentInfo
```typescript
{
  hallTicket: string;
  name: string;
  program: string;
}
```

### Subject
```typescript
{
  code: string;
  name: string;
  credits: string;
  grade: string;
  marks?: string;
}
```

### SemesterInfo
```typescript
{
  gpa?: number;
  semester?: number;
}
```

### Analytics
```typescript
{
  gpa: number;
  performanceLevel: string;
  totalSubjects: number;
  passFailStatus: {
    passed: number;
    failed: number;
    overallStatus: "Pass" | "Fail";
    failedSubjects: Subject[];
  };
  gradeDistribution: {
    [grade: string]: number;
  };
}
```

---

## Error Handling

All errors follow this format:
```json
{
  "error": "Human-readable error message"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found (no results)
- `500`: Internal Server Error

---

## Rate Limiting
Currently no rate limiting. Recommended for production:
- 100 requests per minute per IP
- 1000 requests per hour per IP

---

## CORS
CORS is enabled for all origins in development.
Production should restrict to specific frontend domains.

---

## Example Usage

### cURL
```bash
# Fetch results
curl -X POST http://localhost:5000/api/fetch-results \
  -H "Content-Type: application/json" \
  -d '{
    "hallTicket": "YOUR_HALL_TICKET",
    "examType": "general",
    "viewType": "All Semesters"
  }'
```

### JavaScript (Fetch API)
```javascript
const response = await fetch('http://localhost:5000/api/fetch-results', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    hallTicket: 'YOUR_HALL_TICKET',
    examType: 'general',
    viewType: 'All Semesters'
  })
});

const data = await response.json();
console.log(data);
```

### Python (requests)
```python
import requests

response = requests.post(
    'http://localhost:5000/api/fetch-results',
    json={
        'hallTicket': 'YOUR_HALL_TICKET',
        'examType': 'general',
        'viewType': 'All Semesters'
    }
)

data = response.json()
print(data)
```

---

## Versioning
Current version: v1.0.1

Future versions will use URL versioning:
- `/api/v1/fetch-results`
- `/api/v2/fetch-results`
