// Password rules shared by Sign Up and Reset Password, shown as a live checklist
export const PASSWORD_RULES = [
    { label: '8–20 characters', test: (p) => p.length >= 8 && p.length <= 20 },
    { label: 'An uppercase letter', test: (p) => /[A-Z]/.test(p) },
    { label: 'A lowercase letter', test: (p) => /[a-z]/.test(p) },
    { label: 'A number', test: (p) => /\d/.test(p) },
]

// For the input's pattern attribute (the browser blocks submitting until it matches)
export const PASSWORD_PATTERN = '(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).{8,20}'
export const PASSWORD_HINT = 'Use 8–20 characters with an uppercase letter, a lowercase letter, and a number.'

export const passwordOk = (p) => PASSWORD_RULES.every((rule) => rule.test(p || ''))

// `dark` for the dark panels (reset page); the default suits the white sign-up box
export const PasswordChecklist = ({ password = '', id = 'password-rules', dark = false, className = '' }) => (
    <ul id={id} className={`grid grid-cols-2 gap-x-4 gap-y-1 text-sm ${className}`} aria-live="polite">
        {PASSWORD_RULES.map((rule) => {
            const ok = rule.test(password)
            const color = ok ? (dark ? 'text-[#C6E83A]' : 'text-green-700') : (dark ? 'text-gray-400' : 'text-gray-500')
            return (
                <li key={rule.label} className={`flex items-center gap-2 ${color}`}>
                    <i className={`fa-solid ${ok ? 'fa-circle-check' : 'fa-circle text-[8px] w-[14px] text-center'}`} aria-hidden="true"></i>
                    <span>{rule.label}<span className="sr-only">{ok ? ' (done)' : ' (not yet)'}</span></span>
                </li>
            )
        })}
    </ul>
)
