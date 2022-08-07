# Database Structure

Database Engine: SQLite

**NOT FINAL**

Note: Monetary values will be in paisa. This allows for easy storage as INTEGER type.

## Users Table

|Field Name|Type|Key|Description|
|---|---|---|---|
|UserID|TEXT|PRI|Username|
|Password|TEXT||Salted Password Hash|
|WeeklyTarget|INTEGER||Weekly Spend Target|

## Transactions / Expenses Table

|Field Name|Type|Key|Description|
|---|---|---|---|
|UserID|TEXT|FOREIGN||
|Cost|INTEGER||Transaction Amount|
|Time|INTEGER||Unix Timestamp|
|Category|TEXT*||Expense Category|
|Description|TEXT|||

\* - Might be changed to other type to allow for custom categories in future.