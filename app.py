# =============================================================================
# HR Employee Attrition – Business Intelligence Dashboard
# Single-file Dash application (frontend + backend combined)
# =============================================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

# ---------------------------------------------------------------------------
# 1. Data Loading & Preprocessing
# ---------------------------------------------------------------------------
DATA_PATH = "WA_Fn-UseC_-HR-Employee-Attrition.csv"

df = pd.read_csv(DATA_PATH)

# Normalise column names (strip BOM / whitespace)
df.columns = df.columns.str.strip().str.lstrip("\ufeff")

# Binary attrition flag
df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)

# Satisfaction label maps
sat_map = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
df["JobSatisfactionLabel"]  = df["JobSatisfaction"].map(sat_map)
df["EnvSatisfactionLabel"]  = df["EnvironmentSatisfaction"].map(sat_map)
df["WLBLabel"]              = df["WorkLifeBalance"].map({1: "Bad", 2: "Good", 3: "Better", 4: "Best"})

# Age band
bins   = [18, 25, 35, 45, 55, 100]
labels = ["18-25", "26-35", "36-45", "46-55", "55+"]
df["AgeBand"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)

# ---------------------------------------------------------------------------
# 2. Global KPI helpers
# ---------------------------------------------------------------------------
TOTAL_EMP      = len(df)
TOTAL_ATTRITED = df["AttritionFlag"].sum()
ATTRITION_RATE = round(TOTAL_ATTRITED / TOTAL_EMP * 100, 2)
AVG_AGE        = round(df["Age"].mean(), 1)
AVG_INCOME     = round(df["MonthlyIncome"].mean(), 0)
AVG_TENURE     = round(df["YearsAtCompany"].mean(), 1)

DEPARTMENTS    = ["All"] + sorted(df["Department"].unique().tolist())
GENDERS        = ["All"] + sorted(df["Gender"].unique().tolist())

# ---------------------------------------------------------------------------
# 3. App Initialisation
# ---------------------------------------------------------------------------
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="HR Attrition Dashboard",
)
server = app.server  # For production WSGI servers


# ---------------------------------------------------------------------------
# 4. Reusable UI helpers
# ---------------------------------------------------------------------------
def kpi_card(title, value, color="primary", icon=""):
    return dbc.Card(
        dbc.CardBody([
            html.P(title, className="text-muted mb-1", style={"fontSize": "0.82rem"}),
            html.H4(f"{icon}{value}", className=f"text-{color} fw-bold mb-0"),
        ]),
        className="shadow-sm border-0 h-100",
    )


# ---------------------------------------------------------------------------
# 5. Layout
# ---------------------------------------------------------------------------
app.layout = dbc.Container(
    fluid=True,
    className="px-4 py-3",
    style={"backgroundColor": "#f4f6f9"},
    children=[

        # ── Header ──────────────────────────────────────────────────────────
        dbc.Row(
            dbc.Col(html.Div([
                html.H2("🏢 HR Employee Attrition Dashboard",
                        className="fw-bold mb-0 text-dark"),
                html.P("IBM HR Analytics · Powered by Plotly Dash",
                       className="text-muted small"),
            ]), width=12),
            className="mb-3 mt-2",
        ),

        # ── Filters ─────────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                html.Label("Department", className="fw-semibold small"),
                dcc.Dropdown(
                    id="filter-dept",
                    options=[{"label": d, "value": d} for d in DEPARTMENTS],
                    value="All",
                    clearable=False,
                ),
            ], md=3),
            dbc.Col([
                html.Label("Gender", className="fw-semibold small"),
                dcc.Dropdown(
                    id="filter-gender",
                    options=[{"label": g, "value": g} for g in GENDERS],
                    value="All",
                    clearable=False,
                ),
            ], md=3),
            dbc.Col([
                html.Label("Age Range", className="fw-semibold small"),
                dcc.RangeSlider(
                    id="filter-age",
                    min=18, max=60, step=1,
                    value=[18, 60],
                    marks={i: str(i) for i in range(18, 61, 7)},
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ], md=6),
        ], className="mb-4 bg-white p-3 rounded shadow-sm"),

        # ── KPI Row ──────────────────────────────────────────────────────────
        dbc.Row(id="kpi-row", className="mb-4 g-3"),

        # ── Row 1: Attrition by Dept | Attrition by Age Band ─────────────
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Attrition by Department", className="fw-semibold"),
                dbc.CardBody(dcc.Graph(id="chart-dept", config={"displayModeBar": False})),
            ], className="shadow-sm border-0"), md=6),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Attrition by Age Band", className="fw-semibold"),
                dbc.CardBody(dcc.Graph(id="chart-age", config={"displayModeBar": False})),
            ], className="shadow-sm border-0"), md=6),
        ], className="mb-4 g-3"),

        # ── Row 2: Overtime Impact | Attrition by Job Role ────────────────
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Overtime vs Attrition", className="fw-semibold"),
                dbc.CardBody(dcc.Graph(id="chart-ot", config={"displayModeBar": False})),
            ], className="shadow-sm border-0"), md=5),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Attrition Rate by Job Role", className="fw-semibold"),
                dbc.CardBody(dcc.Graph(id="chart-role", config={"displayModeBar": False})),
            ], className="shadow-sm border-0"), md=7),
        ], className="mb-4 g-3"),

        # ── Row 3: Monthly Income Distribution | Job Satisfaction ─────────
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Monthly Income Distribution (Attrition vs Retained)",
                               className="fw-semibold"),
                dbc.CardBody(dcc.Graph(id="chart-income", config={"displayModeBar": False})),
            ], className="shadow-sm border-0"), md=6),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Job Satisfaction vs Attrition", className="fw-semibold"),
                dbc.CardBody(dcc.Graph(id="chart-jobsat", config={"displayModeBar": False})),
            ], className="shadow-sm border-0"), md=6),
        ], className="mb-4 g-3"),

        # ── Row 4: Marital Status | Business Travel ───────────────────────
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Attrition by Marital Status", className="fw-semibold"),
                dbc.CardBody(dcc.Graph(id="chart-marital", config={"displayModeBar": False})),
            ], className="shadow-sm border-0"), md=4),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Attrition by Business Travel Frequency",
                               className="fw-semibold"),
                dbc.CardBody(dcc.Graph(id="chart-travel", config={"displayModeBar": False})),
            ], className="shadow-sm border-0"), md=4),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Work-Life Balance vs Attrition", className="fw-semibold"),
                dbc.CardBody(dcc.Graph(id="chart-wlb", config={"displayModeBar": False})),
            ], className="shadow-sm border-0"), md=4),
        ], className="mb-4 g-3"),

        # ── Row 5: Heatmap – Years at Company vs Job Level ────────────────
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Attrition Heatmap: Years at Company × Job Level",
                               className="fw-semibold"),
                dbc.CardBody(dcc.Graph(id="chart-heatmap", config={"displayModeBar": False})),
            ], className="shadow-sm border-0"), md=12),
        ], className="mb-4 g-3"),

        # ── Row 6: Detailed Data Table ────────────────────────────────────
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Employee Detail Table (filtered)", className="fw-semibold"),
                dbc.CardBody(
                    dash_table.DataTable(
                        id="detail-table",
                        columns=[
                            {"name": c, "id": c}
                            for c in ["EmployeeNumber", "Age", "Gender", "Department",
                                      "JobRole", "MonthlyIncome", "YearsAtCompany",
                                      "OverTime", "Attrition"]
                        ],
                        page_size=10,
                        style_table={"overflowX": "auto"},
                        style_cell={"fontSize": "0.82rem", "padding": "6px"},
                        style_header={"backgroundColor": "#3b82d4",
                                      "color": "white", "fontWeight": "bold"},
                        style_data_conditional=[{
                            "if": {"filter_query": '{Attrition} = "Yes"'},
                            "backgroundColor": "#fff3f3",
                            "color": "#c0392b",
                        }],
                        sort_action="native",
                        filter_action="native",
                    )
                ),
            ], className="shadow-sm border-0"), md=12),
        ], className="mb-4"),

        # ── Footer ───────────────────────────────────────────────────────
        dbc.Row(dbc.Col(
            html.P("IBM HR Analytics Dashboard · Built with Plotly Dash · IBM Internship Project",
                   className="text-center text-muted small py-2"),
        )),
    ],
)


# ---------------------------------------------------------------------------
# 6. Callbacks
# ---------------------------------------------------------------------------
def filter_df(dept, gender, age_range):
    dff = df.copy()
    if dept != "All":
        dff = dff[dff["Department"] == dept]
    if gender != "All":
        dff = dff[dff["Gender"] == gender]
    dff = dff[(dff["Age"] >= age_range[0]) & (dff["Age"] <= age_range[1])]
    return dff


@app.callback(
    Output("kpi-row", "children"),
    Output("chart-dept",    "figure"),
    Output("chart-age",     "figure"),
    Output("chart-ot",      "figure"),
    Output("chart-role",    "figure"),
    Output("chart-income",  "figure"),
    Output("chart-jobsat",  "figure"),
    Output("chart-marital", "figure"),
    Output("chart-travel",  "figure"),
    Output("chart-wlb",     "figure"),
    Output("chart-heatmap", "figure"),
    Output("detail-table",  "data"),
    Input("filter-dept",   "value"),
    Input("filter-gender", "value"),
    Input("filter-age",    "value"),
)
def update_dashboard(dept, gender, age_range):
    dff = filter_df(dept, gender, age_range)

    total      = len(dff)
    attrited   = dff["AttritionFlag"].sum()
    attr_rate  = round(attrited / total * 100, 2) if total else 0
    avg_income = round(dff["MonthlyIncome"].mean(), 0) if total else 0
    avg_tenure = round(dff["YearsAtCompany"].mean(), 1) if total else 0
    avg_age    = round(dff["Age"].mean(), 1) if total else 0

    # ── KPIs ──────────────────────────────────────────────────────────────
    kpis = dbc.Row([
        dbc.Col(kpi_card("Total Employees",   total,         "dark"),    md=2),
        dbc.Col(kpi_card("Attrited",          attrited,      "danger"),  md=2),
        dbc.Col(kpi_card("Attrition Rate",    f"{attr_rate}%","warning"),md=2),
        dbc.Col(kpi_card("Avg Monthly Income",f"${avg_income:,.0f}","success"), md=2),
        dbc.Col(kpi_card("Avg Tenure (yrs)",  avg_tenure,    "info"),    md=2),
        dbc.Col(kpi_card("Avg Age",           avg_age,       "primary"), md=2),
    ], className="g-3")

    PALETTE = {"Yes": "#e74c3c", "No": "#2ecc71"}

    # ── Chart: Attrition by Department ────────────────────────────────────
    dept_df = (dff.groupby(["Department", "Attrition"])
                  .size().reset_index(name="Count"))
    fig_dept = px.bar(dept_df, x="Department", y="Count", color="Attrition",
                      barmode="group", color_discrete_map=PALETTE,
                      template="plotly_white")
    fig_dept.update_layout(legend_title="Attrition", margin=dict(t=20, b=20))

    # ── Chart: Attrition by Age Band ──────────────────────────────────────
    age_df = (dff.groupby(["AgeBand", "Attrition"])
                 .size().reset_index(name="Count"))
    fig_age = px.bar(age_df, x="AgeBand", y="Count", color="Attrition",
                     barmode="stack", color_discrete_map=PALETTE,
                     template="plotly_white",
                     category_orders={"AgeBand": ["18-25","26-35","36-45","46-55","55+"]})
    fig_age.update_layout(legend_title="Attrition", margin=dict(t=20, b=20))

    # ── Chart: Overtime vs Attrition ──────────────────────────────────────
    ot_df = (dff.groupby(["OverTime", "Attrition"])
                .size().reset_index(name="Count"))
    fig_ot = px.pie(ot_df, names="Attrition", values="Count",
                    facet_col="OverTime",
                    color="Attrition", color_discrete_map=PALETTE,
                    template="plotly_white", hole=0.4)
    fig_ot.update_layout(margin=dict(t=30, b=10))

    # ── Chart: Attrition Rate by Job Role ─────────────────────────────────
    role_df = (dff.groupby("JobRole")
                  .agg(Total=("AttritionFlag", "count"),
                       Attrited=("AttritionFlag", "sum"))
                  .reset_index())
    role_df["Rate"] = round(role_df["Attrited"] / role_df["Total"] * 100, 1)
    role_df.sort_values("Rate", ascending=True, inplace=True)
    fig_role = px.bar(role_df, x="Rate", y="JobRole", orientation="h",
                      text="Rate", template="plotly_white",
                      color="Rate", color_continuous_scale="Reds")
    fig_role.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_role.update_layout(margin=dict(t=20, b=20), coloraxis_showscale=False)

    # ── Chart: Income Distribution ────────────────────────────────────────
    fig_income = px.box(dff, x="Attrition", y="MonthlyIncome",
                        color="Attrition", color_discrete_map=PALETTE,
                        template="plotly_white", points="outliers")
    fig_income.update_layout(legend_title="Attrition", margin=dict(t=20, b=20))

    # ── Chart: Job Satisfaction vs Attrition ──────────────────────────────
    js_df = (dff.groupby(["JobSatisfactionLabel", "Attrition"])
                .size().reset_index(name="Count"))
    fig_jobsat = px.bar(js_df, x="JobSatisfactionLabel", y="Count", color="Attrition",
                        barmode="group", color_discrete_map=PALETTE,
                        template="plotly_white",
                        category_orders={"JobSatisfactionLabel":
                                         ["Low","Medium","High","Very High"]})
    fig_jobsat.update_layout(margin=dict(t=20, b=20))

    # ── Chart: Marital Status ─────────────────────────────────────────────
    mar_df = (dff.groupby(["MaritalStatus", "Attrition"])
                 .size().reset_index(name="Count"))
    fig_marital = px.bar(mar_df, x="MaritalStatus", y="Count", color="Attrition",
                         barmode="stack", color_discrete_map=PALETTE,
                         template="plotly_white")
    fig_marital.update_layout(margin=dict(t=20, b=20))

    # ── Chart: Business Travel ────────────────────────────────────────────
    trav_df = (dff.groupby(["BusinessTravel", "Attrition"])
                  .size().reset_index(name="Count"))
    fig_travel = px.bar(trav_df, x="BusinessTravel", y="Count", color="Attrition",
                        barmode="group", color_discrete_map=PALETTE,
                        template="plotly_white")
    fig_travel.update_layout(margin=dict(t=20, b=20))

    # ── Chart: Work-Life Balance ──────────────────────────────────────────
    wlb_df = (dff.groupby(["WLBLabel", "Attrition"])
                 .size().reset_index(name="Count"))
    fig_wlb = px.bar(wlb_df, x="WLBLabel", y="Count", color="Attrition",
                     barmode="group", color_discrete_map=PALETTE,
                     template="plotly_white",
                     category_orders={"WLBLabel": ["Bad","Good","Better","Best"]})
    fig_wlb.update_layout(margin=dict(t=20, b=20))

    # ── Chart: Heatmap Years@Company × Job Level ──────────────────────────
    heat_df = (dff[dff["Attrition"] == "Yes"]
                  .groupby(["YearsAtCompany", "JobLevel"])
                  .size().reset_index(name="Attrited"))
    heat_pivot = heat_df.pivot(index="JobLevel", columns="YearsAtCompany",
                               values="Attrited").fillna(0)
    fig_heat = px.imshow(heat_pivot, aspect="auto",
                         color_continuous_scale="Reds",
                         labels=dict(x="Years at Company", y="Job Level",
                                     color="Attrited"),
                         template="plotly_white")
    fig_heat.update_layout(margin=dict(t=20, b=20))

    # ── Detail table data ─────────────────────────────────────────────────
    table_data = dff[["EmployeeNumber", "Age", "Gender", "Department",
                       "JobRole", "MonthlyIncome", "YearsAtCompany",
                       "OverTime", "Attrition"]].to_dict("records")

    return (kpis, fig_dept, fig_age, fig_ot, fig_role, fig_income,
            fig_jobsat, fig_marital, fig_travel, fig_wlb, fig_heat, table_data)


# ---------------------------------------------------------------------------
# 7. Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
