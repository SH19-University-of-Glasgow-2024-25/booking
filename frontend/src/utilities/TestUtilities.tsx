import { screen } from "@testing-library/react";

const checkVisible = (ids: string[]): void => {
    ids.forEach((id) => {
        expect(screen.getByTestId(id)).toBeVisible();
    });
};

const checkNull = (ids: string[]): void => {
    ids.forEach((id) => {
        expect(screen.queryByTestId(id)).toBeNull();
    });
};

export {checkNull, checkVisible}