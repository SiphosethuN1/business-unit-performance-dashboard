USE PortfolioAnalytics;
GO

/*==============================================================
  Procedure: dbo.sp_GetBusinessUnitPerformance
  Purpose:
      Returns business unit KPI performance data for reporting
      and Power BI dashboard development.

  Source:
      dbo.business_unit_performance

  Usage:
      EXEC dbo.sp_GetBusinessUnitPerformance;
==============================================================*/

CREATE OR ALTER PROCEDURE dbo.sp_GetBusinessUnitPerformance
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        -- Business Unit Overview
        [Business Unit]                       AS BusinessUnit,
        [Total Resources]                     AS TotalResources,
        [Target]                              AS ActivityTarget,
        [Growth]                              AS ActivityGrowth,

        -- Transaction Value Performance
        [IT & OT Value Target]                AS TransactionValueTarget,
        [PM IT & OT Value]                    AS PreviousMonthTransactionValue,
        [CM IT & OT Value]                    AS CurrentMonthTransactionValue,

        -- Value Added Services
        [VAS]                                 AS ValueAddedServices,

        -- Internal Services Performance
        [IS Target]                           AS InternalServicesTarget,
        [PM IS]                               AS PreviousMonthInternalServices,
        [CW IS]                               AS CurrentInternalServices,
        [Internal Service Target]             AS InternalServiceValueTarget,
        [Count of Internal Services]          AS InternalServiceCount,

        -- External Services
        [ES Value]                            AS ExternalServicesValue,

        -- Incoming Transaction Performance
        [Unique Incoming Transaction Target]  AS IncomingTransactionTarget,
        [Incoming Transaction]                AS IncomingTransactionActual,

        -- Digital Product Performance
        [Unique Digital Product Target]       AS DigitalProductTarget,
        [Unique Digital Product]              AS DigitalProductActual,

        -- Utility Services Performance
        [Utility Service Count]               AS UtilityServiceCount,
        [Utility Service Target]              AS UtilityServiceTarget,
        [Utility Service Value ]              AS UtilityServiceValue

    FROM dbo.business_unit_performance
	WHERE [Business Unit] <> 'Grand Total';

END;
GO