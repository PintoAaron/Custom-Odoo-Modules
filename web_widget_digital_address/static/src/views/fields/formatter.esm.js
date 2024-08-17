/** @odoo-module **/

export function formatDigitalAddress(value) {
    value = value.replace(/-/g, '');       
    const letters = value.slice(0, 2);        
    const divider = Math.floor((value.length - 2) / 2);        
    const firstDigitGroup = value.slice(2, 2 + divider);
    const lastDigitGroup = value.slice(2 + divider);        
    return `${letters.toUpperCase()}-${firstDigitGroup}-${lastDigitGroup}`;
}