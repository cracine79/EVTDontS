// Draws a question's figure: a graph or table described as data (question.figure),
// or the older uploaded picture (question.image_url) when there's no figure.
//
// Graph figure, coordinates in the graph's own units (0..x.max, 0..y.max):
// {
//   "type": "graph",
//   "alt": "What the graph shows, for screen readers",
//   "x": {"label": "Quantity", "max": 10},  "y": {"label": "Price", "max": 10},   // "\n" in a label = new line
//   "curves": [
//     {"label": "Demand", "points": [[0, 9], [8.5, 0.5]], "color": "demand"},    // straight segments
//     {"label": "PPC", "ppc": [8, 7], "bow": 2, "dashed": true, "labelAt": [6, 6]} // production possibilities curve
//   ],                                // ppc = [x-intercept, y-intercept]; bow 1 = straight line, 2 = bowed out
//   "guides": [[[0, 7], [6, 7]]],                 // dashed lines, each a list of points
//   "arrows": [{"from": [4, 4], "to": [5.5, 5.5]}],
//   "xTicks": [[2, "Q1"]],  "yTicks": [[7, "P4"]],
//   "points": [{"at": [2, 7], "label": "A", "pos": "ne"},       // pos: n ne e se s sw w nw
//              {"on": 1, "x": 3, "label": "B", "dot": true}],    // "on" = a point on curve 1 at this x
//   "areas": [{"points": [[0, 9], [2, 7], [0, 7]], "color": "demand", "label": "CS"}],
//   "origin": "0"
// }
// Side-by-side graphs: {"type": "panels", "alt": "...", "panels": [{...graph, "caption": "Figure A"}, ...]}
// Table figure:
// {"type": "table", "caption": "...", "columns": ["Price", "Qd"], "rows": [["$5", 10], ["$4", 12]]}

import { useId } from "react"

const COLORS = {
    demand: '#D62F2F', supply: '#1F5FD1', black: '#1A1A1A', green: '#1E8E3E',
    purple: '#7B3FC4', orange: '#E07400', gray: '#6B7280',
}
const color = (c) => COLORS[c] || c || COLORS.black

const W = 480, H = 440, LEFT = 56, RIGHT = 84, LINE = 19   // SVG units; it scales to fit its box

const OFFSETS = {   // where a point's label sits relative to the point: [dx, dy, text-anchor]
    n: [0, -9, 'middle'], ne: [7, -8, 'start'], e: [9, 5, 'start'], se: [7, 17, 'start'],
    s: [0, 20, 'middle'], sw: [-7, 17, 'end'], w: [-9, 5, 'end'], nw: [-7, -8, 'end'],
}

// A production possibilities curve from (a, 0) to (0, b): (x/a)^n + (y/b)^n = 1
const ppcPoints = ([a, b], n = 2, steps = 48) => Array.from({ length: steps + 1 }, (_, i) => {
    const t = (i / steps) * (Math.PI / 2)
    return [a * Math.pow(Math.cos(t), 2 / n), b * Math.pow(Math.sin(t), 2 / n)]
})

// The curve's height at x (PPC formula, or straight-line interpolation between its points)
const curveY = (c, x) => {
    if (c.ppc) {
        const [a, b] = c.ppc, n = c.bow ?? 2
        return b * Math.pow(Math.max(0, 1 - Math.pow(x / a, n)), 1 / n)
    }
    const pts = [...c.points].sort((p, q) => p[0] - q[0])
    for (let i = 1; i < pts.length; i++) {
        const [x0, y0] = pts[i - 1], [x1, y1] = pts[i]
        if (x >= x0 && x <= x1) return x1 === x0 ? y0 : y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
    }
    return pts[pts.length - 1][1]
}

const Lines = ({ text, x, y, up = false, ...rest }) => {
    const lines = String(text ?? '').split('\n')
    const first = up ? y - (lines.length - 1) * LINE : y
    return <text x={x} y={first} {...rest}>{lines.map((l, i) => <tspan key={i} x={x} dy={i ? LINE : 0}>{l}</tspan>)}</text>
}

const EconGraph = ({ fig, title = true }) => {
    const xMax = fig.x?.max ?? 10, yMax = fig.y?.max ?? 10
    const yLines = String(fig.y?.label ?? '').split('\n').length
    const xLines = String(fig.x?.label ?? '').split('\n').length
    const TOP = 34 + (yLines - 1) * LINE, BOTTOM = 52 + (xLines - 1) * LINE
    const PW = W - LEFT - RIGHT, PH = H - TOP - BOTTOM
    const height = H + (yLines - 1) * LINE + (xLines - 1) * LINE
    const sx = (x) => LEFT + (x / xMax) * PW
    const sy = (y) => TOP + PH - (y / yMax) * PH
    const path = (pts) => pts.map(([x, y], i) => `${i ? 'L' : 'M'}${sx(x)},${sy(y)}`).join(' ')
    const baseY = TOP + PH
    const curves = (fig.curves || []).map((c) => ({ ...c, pts: c.ppc ? ppcPoints(c.ppc, c.bow ?? 2) : c.points }))
    const pointAt = (p) => (p.on != null && curves[p.on] ? [p.x, curveY(curves[p.on], p.x)] : p.at)
    const ids = `arrow${useId().replace(/:/g, '')}`

    return (
        <svg viewBox={`0 0 ${W} ${height}`} role={title ? 'img' : undefined} aria-label={title ? (fig.alt || 'Graph') : undefined}
            className="w-full h-auto block" fontFamily="inherit" fontSize="16" fill="#1A1A1A">
            {title && <title>{fig.alt || 'Graph'}</title>}
            <defs>
                <marker id={ids} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                    <path d="M0,0 L10,5 L0,10 z" fill="#1A1A1A" />
                </marker>
            </defs>

            {(fig.areas || []).map((a, i) => (
                <polygon key={`a${i}`} points={a.points.map(([x, y]) => `${sx(x)},${sy(y)}`).join(' ')}
                    fill={color(a.color)} fillOpacity="0.18" stroke="none" />
            ))}

            {(fig.guides || []).map((g, i) => (
                <path key={`g${i}`} d={path(g)} fill="none" stroke="#1A1A1A" strokeWidth="1.2" strokeDasharray="6 5" />
            ))}

            {/* axes */}
            <path d={`M${LEFT},${TOP - 6} V${baseY} H${LEFT + PW + 8}`} fill="none" stroke="#1A1A1A" strokeWidth="1.6" />
            <Lines text={fig.y?.label} x={LEFT - 8} y={TOP - 14} up textAnchor="start" fontSize="17" />
            <Lines text={fig.x?.label} x={LEFT + PW + 8} y={baseY + 42} textAnchor="end" fontSize="17" />
            {fig.origin != null && <text x={LEFT - 10} y={baseY + 22} textAnchor="end">{fig.origin}</text>}

            {(fig.xTicks || []).map(([x, label], i) => (
                <text key={`xt${i}`} x={sx(x)} y={baseY + 22} textAnchor="middle">{label}</text>
            ))}
            {(fig.yTicks || []).map(([y, label], i) => (
                <text key={`yt${i}`} x={LEFT - 10} y={sy(y) + 5} textAnchor="end">{label}</text>
            ))}

            {curves.map((c, i) => {
                const mid = c.ppc ? c.pts[Math.round(c.pts.length * 0.3)] : c.pts[c.pts.length - 1]
                const [lx, ly] = c.labelAt || mid
                const auto = !c.labelAt
                return (
                    <g key={`c${i}`}>
                        <path d={path(c.pts)} fill="none" stroke={color(c.color)} strokeWidth="2.6" strokeLinejoin="round"
                            strokeDasharray={c.dashed ? '9 6' : undefined} />
                        {c.label && <text x={sx(lx) + (auto ? 8 : 0)} y={sy(ly) + (auto && c.ppc ? -6 : 5)} textAnchor="start"
                            fill={color(c.color)} fontWeight="600">{c.label}</text>}
                    </g>
                )
            })}

            {(fig.arrows || []).map((a, i) => (
                <line key={`ar${i}`} x1={sx(a.from[0])} y1={sy(a.from[1])} x2={sx(a.to[0])} y2={sy(a.to[1])}
                    stroke="#1A1A1A" strokeWidth="1.8" markerEnd={`url(#${ids})`} />
            ))}

            {(fig.areas || []).filter((a) => a.label).map((a, i) => {
                const cx = a.points.reduce((s, p) => s + p[0], 0) / a.points.length
                const cy = a.points.reduce((s, p) => s + p[1], 0) / a.points.length
                const [lx, ly] = a.labelAt || [cx, cy]
                return <text key={`al${i}`} x={sx(lx)} y={sy(ly) + 5} textAnchor="middle" fontWeight="600">{a.label}</text>
            })}

            {(fig.points || []).map((p, i) => {
                const [x, y] = pointAt(p)
                const [dx, dy, anchor] = OFFSETS[p.pos || 'ne'] || OFFSETS.ne
                const gap = p.dot ? 4 : 0
                return (
                    <g key={`p${i}`}>
                        {p.dot && <circle cx={sx(x)} cy={sy(y)} r="7" fill={color(p.color || 'supply')} />}
                        <text x={sx(x) + dx + Math.sign(dx) * gap} y={sy(y) + dy + Math.sign(dy) * gap} textAnchor={anchor}
                            fontWeight="600">{p.label}</text>
                    </g>
                )
            })}
        </svg>
    )
}

const Panels = ({ fig }) => (
    <div role="img" aria-label={fig.alt || 'Graphs'} className="grid grid-cols-2 gap-3">
        {fig.panels.map((p, i) => (
            <div key={i}>
                <EconGraph fig={p} title={false} />
                {p.caption && <p className="text-center text-sm font-semibold text-[#1A1A1A] mt-1">{p.caption}</p>}
            </div>
        ))}
    </div>
)

const DataTable = ({ fig }) => (
    <table className="w-full text-center text-[#1A1A1A] border-collapse">
        {fig.caption && <caption className="pb-2 font-semibold">{fig.caption}</caption>}
        <thead>
            <tr>{fig.columns.map((c, i) => <th key={i} scope="col" className="border-b-2 border-[#1A1A1A] px-3 py-1.5">{c}</th>)}</tr>
        </thead>
        <tbody>
            {fig.rows.map((row, r) => (
                <tr key={r} className="even:bg-black/5">
                    {row.map((cell, i) => <td key={i} className="border-b border-black/15 px-3 py-1.5">{cell}</td>)}
                </tr>
            ))}
        </tbody>
    </table>
)

const FIGURES = { graph: EconGraph, panels: Panels, table: DataTable }

export const QuestionFigure = ({ question, className = '' }) => {
    const fig = question?.figure
    const Figure = FIGURES[fig?.type]
    if (Figure) {
        // Side-by-side graphs need more room than a single one
        const cls = fig.type === 'panels' ? className.replace(/max-w-\S+/, 'max-w-2xl') : className
        return <figure className={`bg-white rounded-xl p-3 ${cls}`}><Figure fig={fig} /></figure>
    }
    if (question?.image_url) {
        return <figure className={`bg-white rounded-xl p-3 ${className}`}><img src={question.image_url} alt="" className="w-full" /></figure>
    }
    return null
}

export default QuestionFigure
